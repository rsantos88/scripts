#!/bin/bash
echo "creating teoSim basicCartesianControl for rightArm"
x-terminal-emulator -e yarpdev --device BasicCartesianControl --name /teoSim/rightArm/CartesianControl --from /usr/local/share/teo-configuration-files/contexts/kinematics/fixedTrunk-rightArm-fetch-kinematics.ini --local /BasicCartesianControl/teoSim/rightArm --remote /teoSim/rightArm --ik st
echo "creating teoSim BasicCartesianControl for leftArm"
x-terminal-emulator -e yarpdev --device BasicCartesianControl --name /teoSim/leftArm/CartesianControl --from /usr/local/share/teo-configuration-files/contexts/kinematics/fixedTrunk-leftArm-fetch-kinematics.ini --local /BasicCartesianControl/teoSim/leftArm --remote /teoSim/leftArm --ik st
echo "creating teoSim BasicCartesianControl for rightLeg (humanoidGait)"
x-terminal-emulator -e yarpdev --device BasicCartesianControl --name /teoSim/rightLeg/CartesianControl --from /usr/local/share/teo-configuration-files/contexts/kinematics/rightLeg-kinematics.ini --local /BasicCartesianControl/teoSim/rightLeg --remote /teoSim/rightLeg --ik st --invKinStrategy humanoidGait
echo "creating teoSim BasicCartesianControl for leftLeg (humanoidGait)"
x-terminal-emulator -e yarpdev --device BasicCartesianControl --name /teoSim/leftLeg/CartesianControl --from /usr/local/share/teo-configuration-files/contexts/kinematics/leftLeg-kinematics.ini --local /BasicCartesianControl/teoSim/leftLeg --remote /teoSim/leftLeg --ik st --invKinStrategy humanoidGait
