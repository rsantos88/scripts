import csv
import math
import sys
import yarp

DELAY = 0.01

robotPrefix = sys.argv[1]
playerPrefix = '/player' + robotPrefix
csvPath = sys.argv[2]

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

options.put('remote', robotPrefix + '/leftArm')
options.put('local', playerPrefix + '/leftArm')
leftArmDevice = yarp.PolyDriver(options)
leftArmEnc = leftArmDevice.viewIEncoders()
leftArmMode = leftArmDevice.viewIControlMode()
leftArmPosd = leftArmDevice.viewIPositionDirect()

options.put('remote', robotPrefix + '/rightArm')
options.put('local', playerPrefix + '/rightArm')
rightArmDevice = yarp.PolyDriver(options)
rightArmEnc = rightArmDevice.viewIEncoders()
rightArmMode = rightArmDevice.viewIControlMode()
rightArmPosd = rightArmDevice.viewIPositionDirect()


options.put('remote', robotPrefix + '/trunk')
options.put('local', playerPrefix + '/trunk')
trunkDevice = yarp.PolyDriver(options)
trunkEnc = trunkDevice.viewIEncoders()
trunkMode = trunkDevice.viewIControlMode()
trunkPosd = trunkDevice.viewIPositionDirect()

leftArmAxes = leftArmEnc.getAxes()
rightArmAxes = rightArmEnc.getAxes()
trunkAxes = trunkEnc.getAxes()

leftArmMode.setControlModes(yarp.IVector(leftArmAxes, yarp.VOCAB_CM_POSITION_DIRECT))
rightArmMode.setControlModes(yarp.IVector(rightArmAxes, yarp.VOCAB_CM_POSITION_DIRECT))
trunkMode.setControlModes(yarp.IVector(trunkAxes, yarp.VOCAB_CM_POSITION_DIRECT))

with open(csvPath, 'r') as csvFile:
    start = yarp.now()
    i = 1
    for row in csv.reader(csvFile):
        if True:
            print(list(map(float, row[:6])))
            print(list(map(float, row[6:13])))
            print(list(map(float, row[13:])))
            leftArmPosd.setPositions(yarp.DVector(list(map(float, row[:6])))) # Division de arreglos
            rightArmPosd.setPositions(yarp.DVector(list(map(float, row[6:12]))))
            trunkPosd.setPositions(yarp.DVector(list(map(float, row[12:]))))
            delay = DELAY * i - (yarp.now() - start)
            yarp.delay(delay)
            i = i + 1

leftArmDevice.close()
rightArmDevice.close()
trunkDevice.close()

yarp.Network.fini()
