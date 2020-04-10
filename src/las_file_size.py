import os

#Allows the User to input path
path_to_las = input(r"Absolute path to the LAS files:")
    
#bytes/point: https://geozoneblog.wordpress.com/2017/09/13/dav-tips-size-estimates/
las_pointsize = 28

#will output the names of the files within the directory
dir_list = os.listdir(path_to_las)

total_points = 0
total_size = 0
for file in dir_list:
    
    if file.endswith(".las"):
        
        file_size = os.path.getsize(os.path.join(path_to_las, file))
        numpoints = file_size//las_pointsize
        total_points += numpoints
        total_size += file_size/1E+12
        os.listdir()

print("Total number of points in the folder is: {:,}".format(total_points))
print("Total number of terabytes in the folder is: {:,.2f}".format(total_size))
