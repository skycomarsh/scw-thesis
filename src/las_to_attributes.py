import subprocess, os
import pandas as pd
import numpy as np
import laspy
import bashlex
import time
from joblib import Parallel, delayed

##### PARAMETERS #########
# USER NEEDS TO INPUT THEIR ABSOLUTE PATH TO THE .LAS FILES
# user = "white"
user = "medeiros"
if user == "medeiros":
    path_to_las = os.path.normpath("/Users/medeiros/Dropbox/ERAU/PROJECTS/DHS_CRC/White_Sky/LidarAnalysis/Job536919_fl2017_lwr_chocta")
    path_to_lastools = os.path.normpath("/Users/medeiros/LAStools/bin/")
    output_location = os.path.normpath("../lasDATA/OUTPUT/")
    dir_list = [f for f in os.listdir(path_to_las) if f.endswith(('las', 'laz'))]
    cores = 8
else:
    path_to_las = r"D:\Franklin_County\LAS"
    dir_list = os.listdir(path_to_las)

pixel_size = 30.0 # meters

def tile_processor(filename):
    print(f"----- working on tile {filename} ---------")
    inputFile = os.path.join(path_to_las, f"{filename}") # input file path
    lasFile=laspy.file.File(inputFile) # create laspy file object
    # create a dataframe for the regression results
    df_out = pd.DataFrame(columns=["filename",
                                "northing",
                                "easting",
                                "sigma_g",
                                "sigma_ng",
                                "ngh"])
    stats_file = os.path.join(output_location, filename[:-3]+"stats")

    # compute tile bounds
    y_start = lasFile.get_y_scaled().min()
    y_end = lasFile.get_y_scaled().max()
    x_start = lasFile.get_x_scaled().min()
    x_end = lasFile.get_x_scaled().max()
    
    for y in np.arange(y_start, y_end, pixel_size):
        for x in np.arange(x_start, x_end, pixel_size):
            output_file = os.path.join(output_location, f"{int(x)}_{int(y)}.txt")
            lastool = os.path.join(path_to_lastools, "las2txt64.exe")
            lastools_commandline = f"wine64 {lastool} -i {inputFile} -inside_tile {x} {y} {pixel_size} -drop_class 9 18 -parse xyzc -sep comma -o {output_file}"
            if user == "medeiros":
                subprocess.run(list(bashlex.split(lastools_commandline)))
            else:
                #NEED TO INPUT USERS PATHS
                os.system(r"..\LAStools\las2txt.exe" \
                r" -i " + inputFile + \
                r" -inside_tile {0} {1} {2} -drop_class 9 18 -o ..\lasOutputData\{0}_{1}.txt" \
                r" -parse xyzc -sep comma" .format(x,y,pixel_size))
            
            df = pd.read_csv(output_file, header=None, names = ['x', 'y', 'z', 'c'])
            # we are now done with the pixel file so we can delete it
            os.remove(output_file)

            df.dropna(inplace = True)
            
            pixel_center = [df.x.mean(), df.y.mean()]
            if np.isnan(pixel_center).any():
                continue

            # localize coordinates
            x0 = df.x.min()
            y0 = df.y.min()
            df.x = df.x - x0
            df.y = df.y - y0

            # extract the ground points LAS class 2 into a new dataframe
            ground_points = df[df.c == 2].reset_index(drop=True)
            # extract the non-ground points LAS class anything except 2 into a new dataframe
            ng_points = df[df.c != 2].reset_index(drop=True)

            numg = len(ground_points)
            numng = len(ng_points)
            if numg == 0:
                continue
            if numng == 0:
                continue
                
            # compute ground point roughness (square root of variance)
            # using ordinary least squares regression plane
            # this is essentially 'by hand', I'm sure there is a python module for this
            A = np.array([[sum([1 for i in ground_points.z]), sum(ground_points.x), sum(ground_points.y)],
                        [sum(ground_points.x), sum(ground_points.x**2), sum(ground_points.x*ground_points.y)],
                        [sum(ground_points.y), sum(ground_points.x*ground_points.y), sum(ground_points.y**2)]])
            b = np.array([sum(ground_points.z), sum(ground_points.x*ground_points.z), sum(ground_points.y*ground_points.z)])

            # if the A matrix is singular, exit the loop and move on to the next pixel
            try:
                beta_g = np.linalg.solve(A,b)      
            except np.linalg.LinAlgError:
                continue

            summation_g = 0.0
            for i in range(numg):
                actual = ground_points.z[i]
                estimated = beta_g[0] + beta_g[1]*ground_points.x[i] + beta_g[2]*ground_points.y[i]
                residual = actual - estimated
                residual_squared = residual**2
                summation_g += residual_squared
            sigma_g = np.sqrt(summation_g)
            
            # compute non-ground point roughness (square root of variance)
            # using ordinary least squares regression plane
            # this is essentially 'by hand', I'm sure there is a python module for this
            A = np.array([[sum([1 for i in ng_points.z]), sum(ng_points.x), sum(ng_points.y)],
                        [sum(ng_points.x), sum(ng_points.x**2), sum(ng_points.x*ng_points.y)],
                        [sum(ng_points.y), sum(ng_points.x*ng_points.y), sum(ng_points.y**2)]])

            b = np.array([sum(ng_points.z),
                        sum(ng_points.x*ng_points.z),
                        sum(ng_points.y*ng_points.z)])

            # if the A matrix is singular, exit the loop and move on to the next pixel
            try:
                beta_ng = np.linalg.solve(A,b)
            except np.linalg.LinAlgError:
                continue

            summation_ng = 0.0
            for i in range(numng):
                actual = ng_points.z[i]
                estimated = beta_ng[0] + beta_ng[1]*ng_points.x[i] + beta_ng[2]*ng_points.y[i]
                residual = actual - estimated
                residual_squared = residual**2
                summation_ng += residual_squared
            sigma_ng = np.sqrt(summation_ng)
            
            # compute height of non-ground regression plane at pixel center
            # note, convert to local coordinates first
            x = pixel_center[0] - x0
            y = pixel_center[1] - y0
            ground_elev_center = beta_g[0] + beta_g[1]*x + beta_g[2]*y
            ng_elev_center = beta_ng[0] + beta_ng[1]*x + beta_ng[2]*y
            ngh = ng_elev_center - ground_elev_center
            df_out = df_out.append({"filename" : filename,
                        "northing" : pixel_center[1],
                        "easting" : pixel_center[0],
                        "sigma_g" : sigma_g,
                        "sigma_ng" : sigma_ng,
                        "ngh" : ngh},
                        ignore_index=True)
        df_out.to_csv(stats_file)

    return print(f"tile {filename} is complete")

if __name__ == '__main__':
    start_time = time.time()
    num_las = len(dir_list)
    print(f"found {num_las} lidar files")

    Parallel(n_jobs=cores)(delayed(tile_processor)(i) for i in dir_list)

    runtime = time.time() - start_time
    print(f"--- {runtime} seconds --- to complete")
    print(f"----- approximately {np.around(runtime/num_las,3)} seconds per las tile ---------")

