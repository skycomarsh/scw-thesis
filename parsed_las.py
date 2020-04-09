import subprocess, os


#path_to_las = input(r"Absolute path to the LAS files:")
os.system(r"C:\Users\skyco\Documents\LAStools\bin\lasview.exe \
lasview -lof file_list.3880.txt -inside_tile 596200 3348700 100 \
las2txt -lof file_list.3880.txt -inside_tile 596200 3348700 100 -odir")
