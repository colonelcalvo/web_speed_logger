###############################################################################
# Web Speed Logger Script
#
# By: Chris Calvo
#
# Notes: This script implements continuously runs speed tests on your internet
#        connection and logs it to a file in ./data. This logger can be stopped
#        by pressing the space bar, at which time the log file that was written to
#        will be passed to two separate scripts to clean up the data and create
#        a new log file with the clean data and the second will take that clean
#        and plot it in a easy to interpret manner.

# Dependencies:
#     - speedtest-cli
###############################################################################

#! /bin/bash

##########################
# Variables
speedTestPeriod=1
filename="../data/speed_test_data.csv"

##########################
# Functions

function print_title_screen () {
  echo ""
  echo "#################################################"
  echo "Welcome to the Web Speed Logger Tool"
  echo "1. Set period between speed tests"
  echo "2. Set filename to write log to"

  echo "3. Start logging"
  echo "4. Clean and plot"
  echo "5. Exit"
  echo -n "Choice: "
}

##########################
# Menu interface

while [ 1 ]
do
  print_title_screen

  read -n 20   # read single user input from terminal
  userInput=$REPLY

  case $userInput in
    "1")
      echo -n "Set period between test in minutes: "
      read -n 20    # read single user input from terminal

      speedTestPeriod=$REPLY
      echo "  Setting period to $speedTestPeriod minutes..."
      ;;
    "2")
      echo -n "Set filename to write to: "
      read -n 40    # read single user input from terminal

      filename=$REPLY
      echo " Set filename to \"$filename\"..."
      ;;
    "3")
      echo "Starting log...: "
      rm -rf $filename
      while [ 1 ]
      do
        REPLY=""
        now=$(date +"%A %F %X")
        speedtest --simple | awk -v now="$now" 'NR==2, NR==3{printf("%s\t%s\t%s\t%s\r\n",now, $1, $2, $3);}' | tee /dev/tty >> $filename
        read -p "Press any letter key to exit..." -n 1 -t 10    # read single user input from terminal
        if [ "$REPLY" != "" ]
        then
          echo "Stopping..."
          break
        fi
        echo ""
      done
      ;;
    "4")
      echo -n "Stating clean and plot on $filename..."
      filename_out="$filename"and"out"
      python speedscript.py -i $filename -o $filename_out
      ;;
    "5")
      echo "Exiting....."
      break
      ;;
  esac
done

##########################
# Clean data w/ python script and plot
