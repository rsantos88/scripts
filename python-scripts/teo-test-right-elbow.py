import csv
import math
import sys
import yarp

# usage: python3 testRightElbow.py /teoSim tests/test_elbow.csv  tests/test_encs.csv

DELAY = 0.01
joint = 3 # elbow

robotPrefix = sys.argv[1]   # prefix
csvInPath = sys.argv[2]     # csv IN csvFile
csvOutPath = sys.argv[3]    # csv OUT csvFile


playerPrefix = '/player' + robotPrefix


if robotPrefix == '/teo':
    isReal = True
elif robotPrefix == '/teoSim':
    isReal = False
else:
    print('error: illegal prefix parameter, choose "/teo" or "/teoSim"')
    quit()

yarp.Network.init()

if not yarp.Network.checkNetwork():
    print('error: please try running yarp server')
    quit()

options = yarp.Property()
options.put('device', 'remote_controlboard')

options.put('remote', robotPrefix + '/rightArm')
options.put('local', playerPrefix + '/rightArm')
rightArmDevice = yarp.PolyDriver(options)
rightArmEnc = rightArmDevice.viewIEncoders()
rightArmMode = rightArmDevice.viewIControlMode()
rightArmPosd = rightArmDevice.viewIPositionDirect()

rightArmAxes = rightArmEnc.getAxes()

# single joint
rightArmMode.setControlMode(joint, yarp.VOCAB_CM_POSITION_DIRECT)

with open(csvInPath, 'r') as csvInFile:
    start = yarp.now()
    i = 1
    csvreader = csv.reader(csvInFile)
    with open(csvOutPath, 'w', newline='') as csvOutfile:
        csvwriter = csv.writer(csvOutfile, delimiter=',')
        csvwriter.writerow(['timestamp', 'value'])
        for row in csvreader:
            if True:
                print('reading >> ', row[3])
                rightArmPosd.setPosition(joint, float(row[3])) # set position
                print('encoder >> ', rightArmEnc.getEncoder(joint))
                csvwriter.writerow([yarp.now(), rightArmEnc.getEncoder(joint)])
                delay = DELAY * i - (yarp.now() - start)
                yarp.delay(delay)
                i = i + 1

rightArmDevice.close()

yarp.Network.fini()
