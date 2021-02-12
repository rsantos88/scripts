
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Raúl de Santos Rico
# Description: Script of a demo where Teo moves the trunk with the aim of stabilizing the neck
# CopyPolicy: released under the terms of the LGPLv2.1
# Python version: 2.7

from time import sleep
import threading
import csv
import yarp # imports YARP

robot = '/teoSim'
timeSpace = 5 # delays between trunk movements
DELAY = 0.01 # IMU sensor reading period
csvFile = "trunk-movements.csv"

#create a new input port and open it
#in_port = yarp.BufferedPortBottle()
#in_port.open("/imusensor/data:i")
#connect up the output port to our input port
#yarp.Network.connect("/imusensor/data:o", "/example/imusensor:i")
#btl = self.in_port.read(True)
#my_data = btl.get(0).asInt()


# YARP
yarp.Network.init()  # connect to YARP network
if yarp.Network.checkNetwork() != True:  # let's see if there was actually a reachable YARP network
    print('[error] Please try running yarp server')  # tell the user to start one with 'yarp server' if there isn't any
    quit()

#-- Trunk (TR)
optionsTR = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsTR.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsTR.put('remote',robot+'/trunk')  # we add info on to whom we will connect
optionsTR.put('local','/demo'+robot+'/trunk')  # we add info on how we will call ourselves on the YARP network
ddTR = yarp.PolyDriver(optionsTR)  # create a YARP multi-use driver with the given options
posTR = ddTR.viewIPositionControl()  # make a position controller object we call 'pos'
encTR = ddTR.viewIEncoders() # encoders
axesTR = posTR.getAxes()  # retrieve number of joints

# Configure acceleration
for joint in range(0, axesTR):
	posTR.setRefAcceleration(joint, 5) # manual por rpc --> set accs (20 20)
# Configure speed
sp = yarp.DVector(axesTR, 5)
posTR.setRefSpeeds(sp)

# writing CSV
def writePossToCsv():
    with open(csvFile, 'w', newline='') as csvOutfile:
        csvwriter = csv.writer(csvOutfile, delimiter=',')
        csvwriter.writerow(['timestamp', 'trunk-joint-1', 'trunk-joint-2'])
        while(1):
            print('timestam: ',round(yarp.now(),3),' [', encTR.getEncoder(0),'], [',encTR.getEncoder(1),']')
            csvwriter.writerow([round(yarp.now(),3), encTR.getEncoder(0), encTR.getEncoder(1)])
            yarp.delay(DELAY)

writingThread = threading.Thread(target = writePossToCsv)
writingThread.start()

# move position
def moveTrunk(axial, frontal):
    tr = yarp.DVector(axesTR,0.0)
    tr = list([axial, frontal])
    posTR.positionMove(yarp.DVector(tr))
    while not posTR.checkMotionDone():
        sleep(0.1)

# Trunk movements
moveTrunk(0,0)
yarp.delay(timeSpace)
moveTrunk(10,10)
yarp.delay(timeSpace)
moveTrunk(20,10)
yarp.delay(timeSpace)
moveTrunk(0,0)
yarp.delay(timeSpace)
