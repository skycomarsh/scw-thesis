import subprocess, os
import laspy
from las_extent import get_X_bounds, get_Y_bounds, get_X_length, get_Y_length, get_x_min, get_x_max, get_y_min, get_y_max

#user defined path to file where .las files saved
path_to_las = input(r"Absolute path to the LAS files:")
dir_list = os.listdir(path_to_las)

#iterating over the defined list
for file in range(len(dir_list)):
   # os.system(r"C:\Program Files\Git\git-bash.exe chmod 777 {}".format(dir_list[x]))

    lasFile=laspy.file.File(os.path.join(path_to_las, "{}".format(dir_list[file])))

    #calling the las_extent functions and defining within this file - adds 2 extra 0's using laspy.File (object)
    x_coord = get_X_bounds(lasFile)[0]/100
    y_coord = get_Y_bounds(lasFile)[0]/100

    inputFile = os.path.join(path_to_las, "{}".format(dir_list[file]))

    y_start = int(round(get_y_min(lasFile)/100))
    y_end = int(round(get_y_max(lasFile)/100))

    x_start = int(round(get_x_min(lasFile)/100))
    x_end = int(round(get_x_max(lasFile)/100))

    #will determine how many files per 
    for y in range(y_start, y_end, 30):
                
        for x in range(x_start, x_end, 30):
           
            os.system(r"C:/Users/skyco/Documents/GitHub/scw-thesis/LAStools/las2txt.exe" \
            r" -i " + inputFile + \
            r" -inside_tile {0} {1} 30 -drop_class 9 18 -o C:/Users/skyco/Documents/GitHub/scw-thesis/lasOutputData/{0}_{1}.txt" \
            r" -parse xyzc -sep comma" .format(x,y))


#FIGURE OUT HOW TO FIX
#os.system(r"..\LAStools\las2txt.exe" \
    #r" -i " + inputFile + \
    #r" -inside_tile {} {} 30 -drop_class 9 -odir ..\lasOutputData -parse xyzc -sep comma".format(x_coord,y_coord))
    #print(command_test)C:\Users\skyco\Documents\LAStestfiles

