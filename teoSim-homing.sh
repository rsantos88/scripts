#!/bin/bash
echo "1) Configuring teoSim to position mode"
echo "set icmd cmds (pos pos pos pos pos pos)" | yarp rpc /teoSim/rightArm/rpc:i
echo "set icmd cmds (pos pos pos pos pos pos)" | yarp rpc /teoSim/leftArm/rpc:i
echo "set icmd cmds (pos pos pos pos pos pos)" | yarp rpc /teoSim/rightLeg/rpc:i
echo "set icmd cmds (pos pos pos pos pos pos)" | yarp rpc /teoSim/leftLeg/rpc:i
echo "2) Doing home position of arms and legs"
echo "set poss (0 0 0 0 0 0)" |  yarp rpc /teoSim/rightArm/rpc:i
echo "set poss (0 0 0 0 0 0)" |  yarp rpc /teoSim/leftArm/rpc:i
echo "set poss (0 0 0 0 0 0)" |  yarp rpc /teoSim/rightLeg/rpc:i
echo "set poss (0 0 0 0 0 0)" |  yarp rpc /teoSim/leftLeg/rpc:i
