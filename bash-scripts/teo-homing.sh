#!/bin/bash
echo "1) Configuring Teo to position mode"
echo "set icmd cmds (pos pos pos pos pos pos pos)" | yarp rpc /teo/rightArm/rpc:i
echo "set icmd cmds (pos pos pos pos pos pos pos)" | yarp rpc /teo/leftArm/rpc:i
echo "set icmd cmds (pos pos pos pos pos pos)" | yarp rpc /teo/rightLeg/rpc:i
echo "set icmd cmds (pos pos pos pos pos pos)" | yarp rpc /teo/leftLeg/rpc:i
echo "2) Doing home position of arms and legs"
echo "set poss (0 0 0 0 0 0 0)" |  yarp rpc /teo/rightArm/rpc:i
echo "set poss (0 0 0 0 0 0 0)" |  yarp rpc /teo/leftArm/rpc:i
echo "set poss (0 0 0 0 0 0)" |  yarp rpc /teo/rightLeg/rpc:i
echo "set poss (0 0 0 0 0 0)" |  yarp rpc /teo/leftLeg/rpc:i
