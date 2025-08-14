#!/bin/bash

# Find Distro
source /etc/os-release
distro=$(echo $PRETTY_NAME | awk 'FS=" " {print $1;}')
# dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# echo $distro
sudo apt-get update 

# Dependencies
dependencies="python3 \
    python3-tk \
    python3-gpiozero \
    tshark"

# Install dependencies, packages
sudo apt-get -y install $dependencies

# Manually install dependencies that fail on Raspberry Pi OS, else install using pip
if [[ $distro = "Debian" ]]; then
    wget https://files.pythonhosted.org/packages/42/70/64a5b11e831dab532b4b61e684c5807a68daeb93b2bd4853975acaaf968e/pycrate-0.7.11.tar.gz
    tar -xzf pycrate-0.7.11.tar.gz
    cd pycrate-0.7.11
    python3 setup.py install
    cd ../
    rm -rf pycrate-0.7.11 pycrate-0.7.11.tar.gz
else 
    sudo apt-get -y install python3-pip
    pip3 install pycrate
fi
