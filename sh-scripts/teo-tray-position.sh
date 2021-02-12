#!/bin/bash
echo "1) Configuring Teo to position mode"
echo "set icmd cmds (pos pos pos pos pos pos pos)" | yarp rpc /teo/rightArm/rpc:i
echo "set icmd cmds (pos pos pos pos pos pos pos)" | yarp rpc /teo/leftArm/rpc:i
echo "2) Doing tray-home position"
echo "set poss (-27.0 -25.5  28.6 -78.7  57.5 -70.6 0)" |  yarp rpc /teo/rightArm/rpc:i
echo "set poss (-27.0  25.5 -28.6 -78.7 -57.5 -70.6 0)" |  yarp rpc /teo/leftArm/rpc:i
