#!/bin/bash
echo -- installation software for teo-manipulation --
echo Updating system...
sudo apt update
echo -e "Updating system... \e[92m[ok]\e[0m"
echo Installing CMake...
sudo apt install cmake
sudo apt install cmake-curses-gui  
echo Installing YCM...
cd  # go home
mkdir -p repos && cd repos  # create $HOME/repos if it doesn't exist; then, enter it
git clone https://github.com/robotology/ycm  # clone repository
mkdir -p ycm/build && cd ycm/build && cmake ..  # configure
make -j$(nproc)  # download external modules
sudo make install && cd  # install and go home
echo -e "Installing YCM... \e[92m[ok]\e[0m"
echo Installing git...
sudo apt install git
git config --global user.name "rsantos88"
git config --global user.email "rasantos@it.uc3m.es"
echo -e "Installing git... \e[92m[ok]\e[0m"
echo Installing Yarp...
sudo apt install build-essential git
sudo apt install libeigen3-dev # Needed for creating YARP lib_math used for kinematics, etc.
sudo apt install qtbase5-dev qtdeclarative5-dev qtmultimedia5-dev qtdeclarative5-qtquick2-plugin qtdeclarative5-window-plugin qtdeclarative5-qtmultimedia-plugin qtdeclarative5-controls-plugin qtdeclarative5-dialogs-plugin libqt5svg5
sudo apt install libjpeg8-dev # Needed for mjpeg carrier
sudo apt install libedit-dev # Enables keyboard arrow keys within an RPC communication channel via terminal
mkdir -p ~/repos; cd ~/repos # Create $HOME/repos if it doesn't exist; then, enter it
git clone https://github.com/robotology/yarp
cd yarp && mkdir build && cd build
cmake .. -DSKIP_ACE=ON -DCREATE_GUIS=ON -DENABLE_yarpcar_mjpeg=ON # configure
make -j$(nproc) # Compile
sudo make install && sudo ldconfig && cd # Install and go home
echo -e "Installing yarp... \e[92m[ok]\e[0m"
echo enabling yarp auto completion...
source ~/repos/yarp/scripts/yarp_completion # Activate in current bash session
echo "source ~/repos/yarp/scripts/yarp_completion" >> ~/.bashrc # Activate in future bash sessions
echo Installing Python bindings...
sudo apt install swig
sudo apt update
sudo apt install libpython-dev # Python development package are not installed by default on clean distros
cd ~/repos/yarp/build
cmake .. -DYARP_COMPILE_BINDINGS=ON -DCREATE_PYTHON=ON
make -j$(nproc)  # compile
sudo make install && sudo ldconfig && cd # Install and go home
echo -e "Installing Python bindings... \e[92m[ok]\e[0m"
echo Installing color debug...
mkdir -p ~/repos && cd ~/repos
git clone https://github.com/roboticslab-uc3m/color-debug 
mkdir -p color-debug/build && cd color-debug/build
make .. && sudo make install
echo -e "Installing color debug... \e[92m[ok]\e[0m"
echo Installing yarp-devices...
cd  # go home
mkdir -p repos; cd repos  # make $HOME/repos if it doesn't exist; then, enter it
git clone https://github.com/roboticslab-uc3m/yarp-devices.git  # Download yarp-devices software from the repository
cd yarp-devices; mkdir build; cd build; cmake ..  # Configure the yarp-devices software
make -j$(nproc)  # Compile
sudo make install  # Install :-)
echo -e "Installing yarp-devices... \e[92m[ok]\e[0m"
sudo ldconfig  # Just in case
echo Installing teo-configuration-files
cd
git clone https://github.com/roboticslab-uc3m/teo-configuration-files
cd teo-configuration-files && mkdir build && cd build
sudo make install
echo -e "Installing teo-configuration-files... \e[92m[ok]\e[0m"
echo -e "\e[2mInstallation completed successfully\e[0m"
