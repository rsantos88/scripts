#!/bin/bash
echo "creating Teo basicCartesianControl for rightArm"
x-terminal-emulator -e yarpdev --device BasicCartesianControl --name /teo/rightArm/CartesianControl --from /usr/local/share/teo-configuration-files/contexts/kinematics/fixedTrunk-rightArm-fetch-kinematics.ini --local /BasicCartesianControl/teo/rightArm --remote /teo/rightArm --ik st
echo "creating Teo BasicCartesianControl for leftArm"
x-terminal-emulator -e yarpdev --device BasicCartesianControl --name /teo/leftArm/CartesianControl --from /usr/local/share/teo-configuration-files/contexts/kinematics/fixedTrunk-leftArm-fetch-kinematics.ini --local /BasicCartesianControl/teo/leftArm --remote /teo/leftArm --ik st
echo "creating Teo BasicCartesianControl for rightLeg (humanoidGait)"
x-terminal-emulator -e yarpdev --device BasicCartesianControl --name /teo/rightLeg/CartesianControl --from /usr/local/share/teo-configuration-files/contexts/kinematics/rightLeg-kinematics.ini --local /BasicCartesianControl/teo/rightLeg --remote /teo/rightLeg --ik st --invKinStrategy humanoidGait
echo "creating Teo BasicCartesianControl for leftLeg (humanoidGait)"
x-terminal-emulator -e yarpdev --device BasicCartesianControl --name /teo/leftLeg/CartesianControl --from /usr/local/share/teo-configuration-files/contexts/kinematics/leftLeg-kinematics.ini --local /BasicCartesianControl/teo/leftLeg --remote /teo/leftLeg --ik st --invKinStrategy humanoidGait
