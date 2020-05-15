import os, subprocess, random, sys
import pandas as pd 
import laspy

#path_to_las = input(r"Absolute path to the LAS files:")
#data=laspy.file.File(r"C:\Users\skyco\Documents\LAStestfiles\16REU955480.las", mode="r")
#datainput=input(r"Input file location with name:")
#data=laspy.file.File(datainput)

def get_X_bounds(data):
    result = list()
    X_min = data.get_x_scaled().min()
    X_max = data.get_x_scaled().max()
    result.append(X_min)
    result.append(X_max)
    return result

def get_x_min(data):
    return data.get_x_scaled().min()

def get_x_max(data):
    return data.get_x_scaled().max()
    
def get_y_min(data):
    return data.get_y_scaled().min()

def get_y_max(data):
    return data.get_y_scaled().max()

def get_Y_bounds(data):
    result = list()
    Y_min = data.get_y_scaled().min()
    Y_max = data.get_y_scaled().max()
    result.append(Y_min)
    result.append(Y_max)
    return result

def get_random_point(bounds):
    randomPoint = random.randrange(bounds[0], bounds[1])
    return randomPoint

def get_X_length(data):
    """returns length of x for file"""
    result = list()
    X_min = data.get_x_scaled().min()
    X_max = data.get_x_scaled().max()
    X_length = X_max - X_min
    result.append(X_length)
    return result

def get_Y_length(data):
    result = list()
    Y_min = data.get_y_scaled().min()
    Y_max = data.get_y_scaled().max()
    Y_length = Y_max - Y_min
    result.append(Y_length)
    return result
    
#get_random_point(get_X_bounds(data))
#sget_random_point(get_Y_bounds(data))

#define LAStools path to be able to access the tools
#lastools_path = "C:\\Users\\whites21\\Desktop\\LAStools"
#las2txt_path = lastools_path + "\\las2txt.exe"
#command = [""+las2txt_path+""]
#os.listdir()


#command.append("-i")
#command.append("C:\\Users\\whites21\\Desktop\\LAS\\Test")

#os.startfile("C:\\Users\\whites21\\Desktop\\LAStools\\bin")
#os.system(r"C:\\Users\\whites21\\Desktop\\LAStools\\bin")

#subprocess.call["C:\Users\whites21\Desktop\LAStools\bin\lasclip.exe"], shell = true)

#subprocess.Popen([r"C:\Users\whites21\Desktop\LAStools\bin\las2txt.exe"])

#subprocess.Popen([r"C:\Users\whites21\Desktop\LAStools\bin\lasview.exe"])

