import re
import time
import datetime

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


if inputblank:
    inputfile = "testfile.txt"
if outputblank:
    outputfile = "testfile_fixed.txt"

print("Using input file: " + inputfile + " and Output file: " + outputfile)


templine = "templine"
workline = "workline"
buildline = "buildline"
prevtimestr = ""
buildtimestr = "buildtime"
morefive = 0
prevtime = datetime.datetime.today()
buildtime = datetime.datetime.today()

open(outputfile, 'w').close()

with open(inputfile, "r") as source:
    with open(outputfile, "w") as sink:
        sink.write("Date Time\tDownload Speed\n")

        for line in source:
            skip_blank=re.search("^\n", line)
            skip_status=re.search("^Passing", line)
            skip_title=re.search("^Starting", line)
            skip_upload=re.search("Upload", line)
            if skip_blank or skip_status or skip_title or skip_upload:
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
                elif cnt == 2:
                    buildline += info + " "
                else :
                    #build the templine
                    buildline += info + "\t"
                cnt += 1
            buildline += "\n"

            buildtimestr = ""
            workline = buildline.replace(" ","\t")
            #print("This is workline before the split " + workline)
            workline = workline.split("\t")

            cnt=1
            for info in workline:
                #print("This is split " + str(cnt) + ": " + info + "\n")
                if cnt == 1:
                    buildtimestr += info + " "
                elif cnt == 2:
                    buildtimestr += info
                else :
                    #build the templine
                    break
                cnt += 1
            #print(buildtimestr)

            if prevtimestr == "":
                prevtimestr = buildtimestr #this is for the first line of time
            else:
                #create time values to compare
                #print("This is previous time string: " + prevtimestr + "\n")
                #print("This is current time string: " + buildtimestr + "\n")
                buildtime = datetime.datetime.strptime(buildtimestr, '%Y-%m-%d %H:%M:%S')
                cnt = 1
                while cnt < 100:
                    prevtime = datetime.datetime.strptime(prevtimestr, '%Y-%m-%d %H:%M:%S')
                    prevtime7 = prevtime + datetime.timedelta(minutes = 7)
                    prevtime5 = prevtime + datetime.timedelta(minutes = 5)
                    prevtime5str = prevtime5.strftime('%Y-%m-%d %H:%M:%S')
                    if prevtime7 < buildtime:
                        sink.write(prevtime5str + "\t0\t\n")
                        prevtimestr = prevtime5str
                        cnt += 1
                    else:
                        break
                prevtimestr = buildtimestr

            sink.write(buildline)
print("Done printing to " + outputfile)
