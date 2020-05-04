import os
import pandas as pd

#user defined path to file where .las files saved
path_to_text = input(r"Absolute path to the LAS files:")
dir_list = os.listdir(path_to_text)

#iterating over the defined list
with open("../statsData/lasFileStatistics.csv", "w") as file:
   
   file.write("File Name, X-Value Mean, Y-Value Mean\n")
   for x in range(len(dir_list)):
   
      inputFile = os.path.join(path_to_text, "{}".format(dir_list[x]))
      
      try:
         df = pd.read_csv(inputFile, header=None)

         file.write("{}".format(dir_list[x]))
         file.write(",")
         file.write(str(df.iloc[:, 0].mean()))
         file.write(",")
         file.write(str(df.iloc[:, 1].mean()))       
         file.write("\n")

      except:
         pass