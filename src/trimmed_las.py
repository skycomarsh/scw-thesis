import subprocess, os
import laspy

#USER NEEDS TO INPUT THEIR ABSOLUTE PATH TO THE .LAS FILES
user = "white"
#user = "medeiros"
if user == "medeiros":
    path_to_las = os.path.normpath("/Users/medeiros/DATA_TEST/LidarAnalysis/test")
    path_to_lastools = os.path.normpath("/Users/medeiros/LAStools/bin/")
    output_location = os.path.normpath("/Users/medeiros/DATA_TEST/LidarAnalysis/OUTPUT/")
    dir_list = [f for f in os.listdir(path_to_las) if f.endswith(('las', 'laz'))]
else:
    path_to_las = r"C:\Users\skyco\Documents\LAStests"
    dir_list = os.listdir(path_to_las)

#iterating over the defined list
for file in range(len(dir_list)):

    lasFile=laspy.file.File(os.path.join(path_to_las, "{}".format(dir_list[file])))

    inputFile = os.path.join(path_to_las, "{}".format(dir_list[file]))
    
    os.system(r"C:\Users\skyco\Documents\LAStools\bin\lasclip.exe" \
    r" -i " + inputFile + \
    r" -poly C:\Users\skyco\Documents\GitHub\scw-thesis\GISfiles\NGOM_RT_v19b_boundaries.shp -drop_class 9 18 -o ..\clippedLAS\{0}.las" \
    r" -interior" .format(inputFile))
    #-v instead of -interior would be outside                

print("COMPLETE")

