# Author: Raul de Santos Rico
# Description: Script of a demo where Teo moves the trunk with the aim of stabilizing the neck
# CopyPolicy: released under the terms of the LGPLv2.1
# Python version: 2.7

from time import sleep
import csv
import yarp # imports YARP

DELAY = 0.01 # IMU sensor reading period
csvFile = "imu.csv"

# YARP
yarp.Network.init()  # connect to YARP network

if yarp.Network.checkNetwork() != True:  # let's see if there was actually a reachable YARP network
    print('[error] Please try running yarp server')  # tell the user to start one with 'yarp server' if there isn't any
    quit()

#create a new input port and open it
in_port = yarp.Port()
in_port.open("/softimu/in")
#connect up the output port to our input port
yarp.Network.connect("/softimu/out", "/softimu/in")

# writing CSV
start = yarp.now()
imu = yarp.Vector(2)

with open(csvFile, 'w') as csvOutfile:
    csvwriter = csv.writer(csvOutfile, delimiter=',')
    csvwriter.writerow(['timestamp','imu-roll', 'imu-pitch'])
    while(1):
        in_port.read(imu)
        print('timestam: ',round(yarp.now()-start,3))
        print('IMU: [', imu[0],', ',imu[1], ']')
        csvwriter.writerow([round(yarp.now()-start,3), imu[0], imu[1]])
        yarp.delay(DELAY)
