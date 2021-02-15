# Author: Raul de Santos Rico
# Description: Script of a demo where Teo moves the trunk with the aim of stabilizing the neck
# CopyPolicy: released under the terms of the LGPLv2.1
# Python version: 2.7

from time import sleep
import threading
import csv
import yarp # imports YARP

robot = '/teo'
timeSpace = 12 # delays between trunk movements
DELAY = 0.01 # IMU sensor reading period
csvFile = "data.csv"

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

#-- softNeck (SN)
optionsSN = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsSN.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsSN.put('remote',robot+'/softNeck')  # we add info on to whom we will connect
optionsSN.put('local','/demo'+robot+'/softNeck')  # we add NSNinfo on how we will call ourselves on the YARP network
ddSN = yarp.PolyDriver(optionsSN)  # create a YARP multi-use driver with the given options
posSN = ddSN.viewIPositionControl()  # make a position controller object we call 'pos'
encSN = ddSN.viewIEncoders() # encoders
axesSN = posSN.getAxes()  # retrieve number of joints

#create a new input port and open it
in_port = yarp.Port()
in_port.open("/softimu/in")
#connect up the output port to our input port
yarp.Network.connect("/softimu/out", "/softimu/in")

# Configure acceleration
for joint in range(0, axesTR):
	posTR.setRefAcceleration(joint, 10) # manual por rpc --> set accs (20 20)

# Configure speed
sp = yarp.DVector(axesTR, 10)
posTR.setRefSpeeds(sp)

# writing CSV
start = yarp.now()
imu = yarp.Vector(2)

def writePossToCsv():
    with open(csvFile, 'w') as csvOutfile:
        csvwriter = csv.writer(csvOutfile, delimiter=',')
        csvwriter.writerow(['timestamp', 'axial-trunk', 'frontal-trunk', 'neck-m1', 'neck-m2', 'neck-m3', 'imu-roll', 'imu-pitch'])
        while(1):
            in_port.read(imu)
            print('timestam: ',round(yarp.now()-start,3))
            print('Trunk encoders: [', encTR.getEncoder(0),'], [',encTR.getEncoder(1),']')
            print('Neck encoders [', encSN.getEncoder(0),', ', encSN.getEncoder(1),', ',encSN.getEncoder(2),']')
            print('IMU: [', imu[0],', ',imu[1], ']')

            csvwriter.writerow([round(yarp.now()-start,3), encTR.getEncoder(0), encTR.getEncoder(1),
                encSN.getEncoder(0), encSN.getEncoder(1), encSN.getEncoder(2),
                imu[0], imu[1]])
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
moveTrunk(20,-12)
yarp.delay(timeSpace)
moveTrunk(0,0)
yarp.delay(timeSpace)
moveTrunk(20,12)
yarp.delay(timeSpace)
moveTrunk(0,0)
yarp.delay(timeSpace)
moveTrunk(-20,-12)
yarp.delay(timeSpace)
moveTrunk(0,0)
yarp.delay(timeSpace)
moveTrunk(-20,12)
yarp.delay(timeSpace)
moveTrunk(0,0)
