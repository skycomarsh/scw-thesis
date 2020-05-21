import subprocess, os
import laspy
from las_extent import get_X_bounds, get_Y_bounds, get_X_length, get_Y_length, get_x_min, get_x_max, get_y_min, get_y_max
import time

start_time = time.time()

#USER NEEDS TO INPUT THEIR ABSOLUTE PATH TO THE .LAS FILES
#user = "white"
user = "medeiros"
if user == "medeiros":
    path_to_las = os.path.normpath("../lasData")
    path_to_lastools = os.path.normpath("/Users/medeiros/LAStools/bin/")
    output_location = os.path.normpath("../lasDATA/OUTPUT/")
    dir_list = [f for f in os.listdir(path_to_las) if f.endswith(('las', 'laz'))]
else:
    path_to_las = r"D:\Franklin_County\LAS"
    dir_list = os.listdir(path_to_las)

pixel_size = 30 # meters, must be an integer

num_las = len(dir_list)
print(f"found {num_las} lidar files")

#iterating over the defined list
for file in range(num_las):
    print(f"----- working on tile {file} of {num_las} ---------")
    lasFile=laspy.file.File(os.path.join(path_to_las, "{}".format(dir_list[file])))

    #calling the las_extent functions and defining within this file - adds 2 extra 0's using laspy.File (object)
    x_coord = get_X_bounds(lasFile)[0]/100
    y_coord = get_Y_bounds(lasFile)[0]/100

    inputFile = os.path.join(path_to_las, "{}".format(dir_list[file]))

    #y_start = int(round(get_y_min(lasFile)/100))
    #y_end = int(round(get_y_max(lasFile)/100))
    #x_start = int(round(get_x_min(lasFile)/100))
    #x_end = int(round(get_x_max(lasFile)/100))
    y_start = int(round(get_y_min(lasFile)))
    y_end = int(round(get_y_max(lasFile)))

    x_start = int(round(get_x_min(lasFile)))
    x_end = int(round(get_x_max(lasFile)))

    #will determine how many files per 
    for y in range(y_start, y_end, pixel_size):
        for x in range(x_start, x_end, pixel_size):
            #print(f"working on pixel {x}, {y}")
            if user == "medeiros":
                lastools_command_string = "wine " + path_to_lastools + \
                "/las2txt64.exe -i " + inputFile + \
                    f" -inside_tile {x} {y} {pixel_size} -drop_class 9 18 -o " + \
                        output_location + f"/{int(x)}_{int(y)}.txt" + " -parse xyzc -sep comma"
                os.system(lastools_command_string)
            else:
                #NEED TO INPUT USERS PATHS
                os.system(r"..\LAStools\las2txt.exe" \
                r" -i " + inputFile + \
                r" -inside_tile {0} {1} {2} -drop_class 9 18 -o ..\lasOutputData\{0}_{1}.txt" \
                r" -parse xyzc -sep comma" .format(x,y,pixel_size))

runtime = time.time() - start_time
print(f"--- {runtime} seconds --- to complete")
print(f"----- approximately {np.around(runtime/num_las,3)} seconds per las tile ---------")

