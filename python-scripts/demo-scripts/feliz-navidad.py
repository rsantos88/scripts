#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Raúl de Santos Rico
# Description: Script of a demo where Teo follows Concha's hand
# Language: Spanish
# CopyPolicy: released under the terms of the LGPLv2.1
# Python version: 2.7

robot = '/teoSim'

from time import sleep
import roboticslab_speech as speech

import _thread

# YARP
import yarp  # imports YARP
yarp.Network.init()  # connect to YARP network
if yarp.Network.checkNetwork() != True:  # let's see if there was actually a reachable YARP network
    print ('[error] Please try running yarp server')  # tell the user to start one with 'yarp server' if there isn't any
    quit()

#-- Left Arm (LA)
optionsLA = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsLA.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsLA.put('remote',robot+'/leftArm')  # we add info on to whom we will connect
optionsLA.put('local','/demo'+robot+'/leftArm')  # we add info on how we will call ourselves on the YARP network
ddLA = yarp.PolyDriver(optionsLA)  # create a YARP multi-use driver with the given options
posLA = ddLA.viewIPositionControl()  # make a position controller object we call 'pos'
llLA = ddLA.viewIControlLimits() # ***********
axesLA = posLA.getAxes()  # retrieve number of joints

#-- Right Arm (RA)
optionsRA = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsRA.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsRA.put('remote',robot+'/rightArm')  # we add info on to whom we will connect
optionsRA.put('local','/demo'+robot+'/rightArm')  # we add info on how we will call ourselves on the YARP network
ddRA = yarp.PolyDriver(optionsRA)  # create a YARP multi-use driver with the given options
posRA = ddRA.viewIPositionControl()  # make a position controller object we call 'pos'
llRA = ddRA.viewIControlLimits() # ***********
axesRA = posRA.getAxes()  # retrieve number of joints

#-- HEAD (H)
optionsH = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsH.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsH.put('remote',robot+'/head')  # we add info on to whom we will connect
optionsH.put('local','/demo'+robot+'/head')  # we add info on how we will call ourselves on the YARP network
ddH = yarp.PolyDriver(optionsH)  # create a YARP multi-use driver with the given options
posH = ddH.viewIPositionControl()  # make a position controller object we call 'pos'
axesH = posH.getAxes()  # retrieve number of joints

#-- Text-to-speech (TTS)
client = yarp.RpcClient()

if not client.open('/demo/tts/rpc:c'):
    print('Unable to open client port %s' % client.getName())
    raise SystemExit

if not yarp.Network.connect('/demo/tts/rpc:c','/tts/rpc:s'):
    print('Unable to connect to remote server port %s' % args.remote)
    raise SystemExit

tts = speech.TextToSpeechIDL()
tts.yarp().attachAsClient(client)

tts.setLanguage('mb-es1')
tts.setSpeed(160) # Values 80 to 450. #170
tts.setPitch(50) # 50 = normal


#-- Pause rutine
import sys, tty, termios
def pause():
    print('in pause...')
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Configure acceleration
for joint in range(0, axesRA):
	posRA.setRefAcceleration(joint, 30) # manual por rpc --> set accs (20 20 20 20 20 20 20 0)
	posLA.setRefAcceleration(joint, 30)

# Configure speed
for joint in range(0, axesRA):
	llRA.setVelLimits(joint, 0, 31) 
	llLA.setVelLimits(joint, 0, 31)
	
sp = yarp.DVector(axesLA, 30)
posRA.setRefSpeeds(sp)
posLA.setRefSpeeds(sp)


# ------ Script ------

la = list([-94, 26, 4, -43.5, -42.6, 0])
posLA.positionMove(yarp.DVector(la))
tts.say('Jou Jou Jou. Soy Teo. El humanoide de la Navidad. Solo queria saludaros y desearos unas felices fiestas')
while not (posLA.checkMotionDone()):
    sleep(0.1)

la = list([-94, 8, 4, -43.5, -65.7, -31.42])
posLA.positionMove(yarp.DVector(la))
while not (posLA.checkMotionDone()):
    sleep(0.1)
    
la = list([0, 0, 0, 0, 0, 0])
posLA.positionMove(yarp.DVector(la))
while not (posLA.checkMotionDone()):
    sleep(0.1)
    
while not (tts.checkSayDone()):
    sleep(0.1)
    
la = list([-37.8, 6, -9.5, -73.23, 0.0, 8.73])
ra = list([-37.8, -6, 9.5, -73.23, 0.0, 8.73])
posLA.positionMove(yarp.DVector(la))
posRA.positionMove(yarp.DVector(ra))
tts.say('sed buenos, comed muchos polvorones y no os atraganteis con las uvas')
while not (posLA.checkMotionDone() and posRA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)
    

la = list([-96, -2, -4, -67.2, -78.1, -54.12])
ra = list([-96,  2,  4, -67.2,  78.1, -54.12])
tts.say('nos vemos el anio que viene por el laboratorio')
posLA.positionMove(yarp.DVector(la))
posRA.positionMove(yarp.DVector(ra))
while not (posLA.checkMotionDone() and posRA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)
    
    
la = list([-37.8, 6, -9.5, -73.23, 0.0, 8.73])
ra = list([-37.8, -6, 9.5, -73.23, 0.0, 8.73])
posLA.positionMove(yarp.DVector(la))
posRA.positionMove(yarp.DVector(ra))
tts.say('jou jou jou, feliz 2023')
while not (posLA.checkMotionDone() and posRA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)
    




# Home

head = yarp.DVector(axesH,0.0)
ra = yarp.DVector(axesRA,0.0)
la = yarp.DVector(axesLA,0.0) 

posH.positionMove(head)
posRA.positionMove(ra)
posLA.positionMove(la)

while not (posLA.checkMotionDone() and posRA.checkMotionDone()):
    sleep(0.1)

