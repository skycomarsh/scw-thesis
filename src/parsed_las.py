import subprocess, os
import laspy
from las_extent import get_X_bounds, get_Y_bounds

#user defined path to file where .las files saved
path_to_las = input(r"Absolute path to the LAS files:")
dir_list = os.listdir(path_to_las)


#iterating over the defined list
for x in range(len(dir_list)):
   # os.system(r"C:\Program Files\Git\git-bash.exe chmod 777 {}".format(dir_list[x]))

    lasFile=laspy.file.File(os.path.join(path_to_las, "{}".format(dir_list[x])))

    #calling the las_extent functions and defining within this file - adds 2 extra 0's using laspy.File (object)
    x_coord = get_X_bounds(lasFile)[0]/100
    y_coord = get_Y_bounds(lasFile)[0]/100

    print(x_coord)
    print(y_coord)

    inputFile = os.path.join(path_to_las, "{}".format(dir_list[x]))

    os.system(r"..\LAStools\las2txt.exe" \
    r" -i " + inputFile + \
    r" -inside_tile {} {} 30 -odir ..\lasOutputData -parse xyzc -sep comma".format(x_coord,y_coord))

    #print(command_test)


#path to the las tools bin with the las function. Will need to edit so las2txt is automatically 
#input and just the bin file location is input.
#lasbin_location = input(r"Path for LAStools bin:")
#lasbin_location=laspy.file.File(lasbin_input)

#path to the las files on each computer. I will need to eventually incorporate 
#automated file selection. Currently you need to input the exact .las file to parse.
#lasfile_location = input(r"Path of .las files to read:")
#lasfile_location=laspy.file.File(lasbin_input)

#Automatically chooses the inside the tile with a tile size of 30x30. 
#For now I'm automatically inputting the bounds #Will need to add 
#in the lasextent.py file to automate. PUT FUCNTION HERE WHEN INTEGRATED.
#(IF WANTED)tilesize_input = input(r"Tile size:")
#tilesize=laspy.file.File(tilesize_input)

#Location for the newly created .txt file from the parsed las file
#lastxt_location = input(r"Path for new .txt file:")
#lastxt_location=laspy.file.File(lastxt_input)

#os.system(r"lasbin_location" \
#r" -i lasfile_location" \
#r" -inside_tile 596000 3349450 30 -odir lastxt_location -parse xyz -sep tab")

