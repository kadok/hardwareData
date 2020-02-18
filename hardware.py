import os
import subprocess
from shlex import split
import json

f = open("hardware.csv", "w")

#System
systemInfo = subprocess.check_output(["sudo","lshw","-class","system","-json"]).decode(encoding="UTF-8")
systemInfo = json.loads(systemInfo,encoding="UTF-8")
if(systemInfo):
    f.write("#System;\n")
    f.write("Id;Product;Vendor;Serial;\n")
    f.write(systemInfo["id"]+";"+systemInfo["product"]+";"+systemInfo["vendor"]+";"+systemInfo["serial"]+";")
    f.write("\n\n")

#Get CPU info
#cpuInfo = subprocess.check_output("cpuinfo").decode(encoding="UTF-8")
cpuInfo = subprocess.check_output(["sudo","lshw","-class","cpu"]).decode(encoding="UTF-8")
cpuInfo = str(cpuInfo)
cpuLines = cpuInfo.split("\n")
f.write("#Processor;\n")
f.write("Description;Product;Vendor;Physical Id;Bus Info;Version;Serial;Slot;Size;Capacity;Width;Clock;\n")
strLine = ""
for i, line in enumerate(cpuLines):
    if '*-cpu' in line:
        for j in range(1,13):
            proc = cpuLines[i+j].split(":")
            if len(proc) > 1:
                strLine += proc[1]+";"    
        f.write(strLine)
        f.write("\n")
        strLine = ""
f.write("\n\n")

#Memory
memoryInfo = subprocess.check_output(["sudo","lshw","-class","memory"]).decode(encoding="UTF-8")
memoryInfo = str(memoryInfo)
memoryLines = memoryInfo.split("\n")
f.write("#Memory;\n")
f.write("Description;Physical Id;Slot;Total Size;Type;\n")
for i, line in enumerate(memoryLines):
    if '*-memory' in line:
        for j in range(1,6):
            proc = memoryLines[i+j].split(":")
            if len(proc) > 1:
                strLine += proc[1]+";"    
        f.write(strLine)
        strLine = "" 
        break 
f.write("\n\n")
f.write("Id;Description;Product;Vendor;Physical Id;Serial;Slot;Size;Width;Clock;\n")
for i, line in enumerate(memoryLines):
    if '*-bank' in line:
        for j in range(0,10):
            proc = memoryLines[i+j].split(":")
            if len(proc) > 1:
                strLine += proc[1]+";"    
        f.write(strLine)
        f.write("\n")
        strLine = ""
f.write("\n\n")

#Motherboard
motherboardInfo = subprocess.check_output(["sudo","dmidecode","-t","2"]).decode(encoding="UTF-8")
motherboardInfo = str(motherboardInfo)
motherboardLines = motherboardInfo.split("\n")
f.write("#Motherboard;\n")
f.write("Manufacturer;Product;Version;Serial;\n")
strLine = ""
for i, line in enumerate(motherboardLines):
    if 'Manufacturer' in line:
        for j in range(0,4):
            proc = motherboardLines[i+j].split(":")
            if len(proc) > 1:
                strLine += proc[1]+";"    
        f.write(strLine)
        strLine = ""
f.write("\n\n")


#Video Board
videoInfo = subprocess.check_output(["sudo","lshw","-class","video"]).decode(encoding="UTF-8")
videoInfo = str(videoInfo)
videoLines = videoInfo.split("\n")
f.write("#Graphic Card;\n")
f.write("Description;Product;Vendor;Physical Id;Bus Info;Version;Width;Clock;\n")
for i, line in enumerate(videoLines):
    if '*-display' in line:
        for j in range(1,9):
            proc = videoLines[i+j].split(":")
            if len(proc) > 1:
                strLine += proc[1]+";"    
        f.write(strLine)
        f.write("\n")
        strLine = "" 
f.write("\n\n")


#Storage
diskInfo = subprocess.check_output(["sudo","lshw","-class","disk"]).decode(encoding="UTF-8")
diskInfo = str(diskInfo)
diskLines = diskInfo.split("\n")
diskId = 0
f.write("#Storage;\n")
f.write("Description;Product;Physical Id;Bus Info;Logical Name;Version;Serial;Size;\n")
for i, line in enumerate(diskLines):
    if '*-disk' in line:
        for j in range(1,9):
            proc = diskLines[i+j].split(":")
            if len(proc) > 1:
                strLine += proc[1]+";"    
        f.write(strLine)
        f.write("\n")
        strLine = "" 
f.write("\n")
f.write("#Media;\n")
f.write("Description;Product;Physical Id;Bus Info;\n")
for i, line in enumerate(diskLines):
    if '*-cdrom' in line:
        for j in range(1,5):
            proc = diskLines[i+j].split(":")
            if len(proc) > 1:
                strLine += proc[1]+";"    
        f.write(strLine)
        f.write("\n")
        strLine = ""
f.write("\n\n")

f.close()