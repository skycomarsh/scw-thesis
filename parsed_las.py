import subprocess, os

#importing os allows powershell commands to be used. Make sure to include the "", \, and r when 
#breaking lines
os.system(r"C:\Users\skyco\Documents\LAStools\bin\las2txt.exe" \
r" -i C:\Users\skyco\Documents\LAStestfiles\16REU955480.las" \
r" -inside_tile 596000 3349450 30 -odir C:\Users\skyco\Documents -parse xyz -sep tab")
