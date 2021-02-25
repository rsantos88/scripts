#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Raúl de Santos Rico
# Description: Script of a demo where Teo is waving to Concha and asks how she is
# Language: Spanish
# CopyPolicy: released under the terms of the LGPLv2.1
# Python version: 2.7

robot = '/teo'

from time import sleep

import thread

# YARP
import yarp  # imports YARP
yarp.Network.init()  # connect to YARP network
if yarp.Network.checkNetwork() != True:  # let's see if there was actually a reachable YARP network
    print '[error] Please try running yarp server'  # tell the user to start one with 'yarp server' if there isn't any
    quit()

#-- Left Arm (LA)
optionsLA = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsLA.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsLA.put('remote',robot+'/leftArm')  # we add info on to whom we will connect
optionsLA.put('local','/demo'+robot+'/leftArm')  # we add info on how we will call ourselves on the YARP network
ddLA = yarp.PolyDriver(optionsLA)  # create a YARP multi-use driver with the given options
posLA = ddLA.viewIPositionControl()  # make a position controller object we call 'pos'
axesLA = posLA.getAxes()  # retrieve number of joints

#-- Right Arm (RA)
optionsRA = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
optionsRA.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
optionsRA.put('remote',robot+'/rightArm')  # we add info on to whom we will connect
optionsRA.put('local','/demo'+robot+'/rightArm')  # we add info on how we will call ourselves on the YARP network
ddRA = yarp.PolyDriver(optionsRA)  # create a YARP multi-use driver with the given options
posRA = ddRA.viewIPositionControl()  # make a position controller object we call 'pos'
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
tts = yarp.RpcClient()
tts.open('/demo/tts/rpc:c')
yarp.Network.connect('/demo/tts/rpc:c','/tts/rpc:s');

def ttsLang(language):
    cmd = yarp.Bottle()
    res = yarp.Bottle()
    cmd.addString('setLanguage')
    cmd.addString(language)
    tts.write(cmd,res)

def ttsSay(sayStr):
    cmd = yarp.Bottle()
    res = yarp.Bottle()
    cmd.addString('say')
    cmd.addString(sayStr)
    tts.write(cmd,res)


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
	posRA.setRefAcceleration(joint, 30) # manual por rpc --> set accs (30 30 30 30 30 30 30 0)
	posLA.setRefAcceleration(joint, 30)

# configure speed
sp = yarp.DVector(axesRA, 30)
posRA.setRefSpeeds(sp)
posLA.setRefSpeeds(sp)

# Configure speech
ttsLang('mb-es1')

# Home

head = yarp.DVector(axesH,0.0)
ra = yarp.DVector(axesRA,0.0)
la = yarp.DVector(axesLA,0.0)

# ------ Script ------
head[0] = -40
posH.positionMove(head)

# pause()
sleep(8)

head[0] = 0
posH.positionMove(head)
ttsSay('estoy identificando a alguien...')
while not posH.checkMotionDone():
    sleep(0.1)

ra = list([-28.57, -13.70, 9.60, -65.34, 0.00, 0.00])
posRA.positionMove(yarp.DVector(ra))
ttsSay('persona identificada, hola Concha, que sorpresa')
ttsSay('como estas?')
while not posRA.checkMotionDone():
    sleep(0.1)

ra[5] = -11
posRA.positionMove(yarp.DVector(ra))
while not posRA.checkMotionDone():
    sleep(0.1)

# new thread: not blocking
thread.start_new_thread(ttsSay,('yo estoy muy bien, gracias, tenía ganas de verte por aquí',))

# salute
for x in range(0,2):
    ra[5] = -11
    posRA.positionMove(yarp.DVector(ra))
    while not posRA.checkMotionDone():
        sleep(0.1)
    ra[5] = 3
    posRA.positionMove(yarp.DVector(ra))
    while not posRA.checkMotionDone():
        sleep(0.1)

# give up left arm and open right arm
h = yarp.DVector(axesH,0.0) 
ra = list([-28.57, -18.70, 9.60, -65.34, 0.00, 0.00])
la = list([-28.57, 18.70, 9.60, -65.34, 0.00, 0.00])
posH.positionMove(h)
posRA.positionMove(yarp.DVector(ra))
posLA.positionMove(yarp.DVector(la))
ttsSay("estoy preparado para comenzar con las pruebas")
while not (posLA.checkMotionDone() and posRA.checkMotionDone() ):
    sleep(0.1)

# question
ra = list([-63.27, -37.20, 9.59, -65.33, 0.00, 15.98])
la = list([-63.27, 37.20, -9.59, -65.33, 0.00, 15.98])
posRA.positionMove(yarp.DVector(ra))
posLA.positionMove(yarp.DVector(la))
ttsSay("por donde quieres que empecemos?")
while not ( posLA.checkMotionDone() and posRA.checkMotionDone() ):
    sleep(0.1)

# new thread: not blocking
thread.start_new_thread(ttsSay,('de acuerdo, cargando sistema de archivos, configuración lista, esperando a recibir comandos de información',))
ra = list([-8.16, -3.91, -16.45, -63.36, 68.40, -55.93])
la = list([-8.16, 3.91, 16.45, -63.36, -68.40, -55.93])
posRA.positionMove(yarp.DVector(ra))
posLA.positionMove(yarp.DVector(la))
while not ( posLA.checkMotionDone() and posRA.checkMotionDone() ):
    sleep(0.1)

# Home
head = yarp.DVector(axesH,0.0)
ra = yarp.DVector(axesRA,0.0)
la = yarp.DVector(axesLA,0.0)
posH.positionMove(head)
posRA.positionMove(ra)
posLA.positionMove(la)
