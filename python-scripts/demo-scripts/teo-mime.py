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
tts.setSpeed(150) # Values 80 to 450.
tts.setPitch(60) # 50 = normal


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
	posRA.setRefAcceleration(joint, 20) # manual por rpc --> set accs (20 20 20 20 20 20 20 0)
	posLA.setRefAcceleration(joint, 20)

# Configure speed

for joint in range(0, axesRA):
	llRA.setVelLimits(joint, 0, 35) 
	llLA.setVelLimits(joint, 0, 35)
	
sp = yarp.DVector(axesLA, 30)
posRA.setRefSpeeds(sp)
posLA.setRefSpeeds(sp)

# Home

head = yarp.DVector(axesH,0.0)
ra = yarp.DVector(axesRA,0.0)
la = yarp.DVector(axesLA,0.0) 

# ------ Script ------
# Right Arm moving

head[0] = -20
posH.positionMove(head)
tts.say('estoy identificando tu mano izquierda')
while not (posH.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)


ra = list([-38.77, -9.79, -10.96, -63.36, -7.20, 8.00])
posRA.positionMove(yarp.DVector(ra))
tts.say('voy, a, seguirla')
while not (posRA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)


head[0] = -40
posH.positionMove(head)
ra = list([-60.00, -9.79, -20.96, -63.36, -7.20, 8.00])
posRA.positionMove(yarp.DVector(ra))
tts.say('estas moviendo tu mano hacia arriba')
while not (posRA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)

head[0] = -30
posH.positionMove(head)
ra = list([-60.39, -9.79, -10.96, -47.52, -7.19, 22.37])
posRA.positionMove(yarp.DVector(ra))
tts.say('ahora la estas moviendo hacia abajo')
while not (posRA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)

head[0] = -35
posH.positionMove(head)
ra = list([-50.77, -9.79, -20.96, -30.0, -7.20, 0.0])
posRA.positionMove(yarp.DVector(ra))
tts.say('un poco más abajo')
while not (posRA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)

head[0] = -40
posH.positionMove(head)
ra = list([-28.57, -9.79, -20.96, -75.24, -7.19, 15.98])
posRA.positionMove(yarp.DVector(ra))
tts.say('estas acercando tu mano izquierda a mi mano')
while not (posRA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)


head[0] = 0
posH.positionMove(head)
ra = list([-28.57, -9.79, -20.96, -75.24, -7.19, 15.98])
posRA.positionMove(yarp.DVector(ra))
tts.say('ahora veo tu mano derecha')
while not (posRA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)

tts.say('calibrando sensores')

head[0] = 20
posH.positionMove(head)
tts.say('sigo viendo tu mano derecha moverse')
while not (posH.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)

# Left arm moving
head[0] = 35
posH.positionMove(head)
la = list([-38.77, 9.79, -10.96, -63.36, -7.20, 8.00])
posLA.positionMove(yarp.DVector(la))
tts.say('voy, a, seguirla')
while not (posLA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)

head[0] = 40
posH.positionMove(head)
la = list([-60.00, 9.79, 20.96, -63.36, -7.20, 8.00])
posLA.positionMove(yarp.DVector(la))
tts.say('estas moviendo tu mano derecha hacia arriba')
while not (posLA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)

head[0] = 30
posH.positionMove(head)
la = list([-60.00, 6.02, 5.42, -63.36, 7.19, 15.71])
posLA.positionMove(yarp.DVector(la))
tts.say('estas moviendo tu mano hacia mi derecha')
while not (posLA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)


head[0] = 20
posH.positionMove(head)
la = list([-60.00, -2.02, 5.42, -63.36, 7.19, 15.74])
posLA.positionMove(yarp.DVector(la))
tts.say('un poco mas a la derecha')
while not (posLA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)

head[0] = 25
posH.positionMove(head)
la = list([-75.6, 2.00, 5.41, -63.36, 7.19, 36.66])
posLA.positionMove(yarp.DVector(la))
tts.say('ahora la estas moviendo hacia arriba')
while not (posLA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)

head[0] = 20
posH.positionMove(head)
la = list([-88.2, 1, 0.0, -20.87, 7.19, 1.74])
posLA.positionMove(yarp.DVector(la))
tts.say('ahora la estas alejando')
while not (posLA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)

head[0] = 0
posH.positionMove(head)
ra = list([-46.94, -24.47, 2.74, -53.46, 0.0, 0.0])
la = list([-46.94, 24.47, 2.74, -53.46, 0.0, 0.0])
posRA.positionMove(yarp.DVector(ra))
posLA.positionMove(yarp.DVector(la))
tts.say('ahora veo tus dos manos. Esto es una locura ')
while not (posLA.checkMotionDone() and posRA.checkMotionDone() and tts.checkSayDone()):
    sleep(0.1)

# Home
head = yarp.DVector(axesH,0.0)
ra = yarp.DVector(axesRA,0.0)
la = yarp.DVector(axesLA,0.0)
posH.positionMove(head)
posRA.positionMove(ra)
posLA.positionMove(la)
tts.say('creo que he tenido suficiente por hoy. Necesito descansar')
