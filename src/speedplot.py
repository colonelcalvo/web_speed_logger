import re
import time
import datetime
import sys, getopt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy

inputfile = ""

argfound = 0
inputfound = 0
inputblank = 1

for argument in sys.argv:
    #print(argument)
    inputfound = re.search("-i", argument)
    if inputfound:
        #print("Input file found")
        argfound = 1
    elif argfound == 1:
        inputfile = argument
        argfound = 0
        inputfound = 0
        inputblank = 0
    else:
        continue


if inputblank:
    inputfile = "testfile.txt"

print("Using input file: " + inputfile)

workline = "hello"
datevector = numpy.array([])
speedvector = numpy.array([])

with open(inputfile, "r") as source:
    cntline = 1
    for line in source:
        workline = line.split("\t")
        cnt=1
        print(line)
        print(workline)
        if cntline != 1:
            for info in workline:
                if cnt == 1:
                    print("building date time")
                    builddate = datetime.datetime.strptime(info, '%Y-%m-%d %H:%M:%S')
                elif cnt == 2:
                    buildspeed = float(info)
                else:
                    break
                cnt += 1
        else:
            cntline += 1
            continue

        datevector = numpy.append(builddate,cntline-1)
        speedvector = numpy.append(buildspeed,cntline-1)
        cntline += 1

print(speedvector)

#fig = plt.figure(figsize=(11, 7))
#plt.plot(speedvector)
#plt.show()
