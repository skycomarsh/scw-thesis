import subprocess, os
import laspy, numpy, statistics

#user defined path to file where .las files saved
path_to_text = input(r"Absolute path to the LAS files:")
dir_list = os.listdir(path_to_text)

#iterating over the defined list
for file in range(len(dir_list)):
   # os.system(r"C:\Program Files\Git\git-bash.exe chmod 777 {}".format(dir_list[x]))
    
    with open('*.txt', 'w') as text_reader: 
        
        for line in file1:

            file2.write(",".join([1])+ '\n')
            xyzc_file = xyzc_open.readlines()
            mean_x = statistics.mean(xyzc_file[1])
            mean_y = statistics.mean(xyzc_file[2])
            mean_z = statistics.mean(xyzc_file [3])

            file.close()


    lasFile=laspy.file.File(os.path.join(path_to_text, "{}".format(dir_list[file])))

    #calling the las_extent functions and defining within this file - adds 2 extra 0's using laspy.File (object)

    inputFile = os.path.join(path_to_text, "{}".format(dir_list[file]))
