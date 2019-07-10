#!/bin/bash
echo "Script: opening yarpview (vision)"
sleep 0.2s
yarpview
yarp connect /xtion/rgbImage:o /yarpview/img:i
