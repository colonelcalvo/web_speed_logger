import re
import time
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy
import sys, getopt

inputfile = ""
outputfile = ""
#arguments = str(sys.argv)
argfound = 0
inputfound = 0
inputblank = 1
outputfound = 0
outputblank = 1

for argument in sys.argv:
    #print(argument)
    inputfound = re.search("-i", argument)
    outputfound = re.search("-o", argument)
    #print("Regex results: " + str(inputfound) + " " + str(outputfound) + " for string: " + argument)
    if inputfound:
        #print("Input file found")
        argfound = 1
    elif outputfound:
        #print("Output file found")
        argfound = 2
    elif argfound == 1:
        inputfile = argument
        argfound = 0
        inputfound = 0
        inputblank = 0
    elif argfound == 2:
        outputfile = argument
        argfound = 0
        outputfound = 0
        outputblank = 0
    else:
        continue


if inputblank==1:
    inputfile = "testfile.txt"
#if outputblank==1:
#    outputfile = "testfile_fixed.txt"

print("Using input file: " + inputfile + " and Output file: " + outputfile)


templine = "templine"
workline = "workline"
buildline = "buildline"
prevtimestr = ""
buildtimestr = "buildtime"
morefive = 0

datevector = numpy.array([])
downspeedvector = numpy.array([])
upspeedvector = numpy.array([])

open(outputfile, 'w').close()

with open(inputfile, "r") as source:
    with open(outputfile, "w") as sink:
        sink.write("Date Time\tDownload Speed\t Upload Speed\n")

        for line in source:
            skip_blank=re.search("^\n", line)
            skip_status=re.search("^Passing", line)
            skip_title=re.search("^Starting", line)
            upload=re.search("Upload", line)
            if skip_blank or skip_status or skip_title:
                #print("Found blank, status, or title")
                continue

            workline = line.replace("\t"," ")
            workline = workline.split(" ")
            cnt=1
            buildline = ""

            for info in workline:
                if cnt == 1 or cnt == 4 or cnt == 6:
                    #skip the first thing, monday etc.
                    x=1
                elif cnt == 2 and upload == None :
                    buildline += info + " "
                elif cnt == 3 and upload == None :
                    buildline += info + "\t"
                elif upload == None:
                    #build the templine
                    buildline += info + "\t"
                elif cnt == 5 and upload != None:
                    buildline += info + "\n"
                else:
                    x=1
                cnt += 1

            cnt=1
            workline = buildline.split("\t")
            print(workline)
            for info in workline:
                print(info)
                if cnt == 1 and info != "\n" and upload == None:
                    datevector = numpy.append(datevector,datetime.strptime(info, "%Y-%m-%d %H:%M:%S"))
                elif cnt == 1 and info != "\n" and upload != None:
                    upspeedvector = numpy.append(upspeedvector,float(info))
                    break
                    #print(buildspeed)
                elif cnt == 2:
                    downspeedvector = numpy.append(downspeedvector,float(info))
                    #print(buildspeed)
                else:
                    break

                cnt += 1

            sink.write(buildline)
print("Done printing to " + outputfile)

fig = plt.figure()
ax1 = fig.subplots()

ax1.plot(datevector,downspeedvector)
ax1.set_ylabel("Download Speed [Mbits/s]", color="blue" )
ax1.set_title("Download Speed VS Date & Time")
ax1.set_xlabel("Date & Time")

ax2 = ax1.twinx()
ax2.plot(datevector,upspeedvector, color="red")
ax2.set_ylabel("Upload Speed [Mbits/s]", color="red")

plt.show()
