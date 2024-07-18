#!/bin/bash

# Find Distro
source /etc/os-release
distro=$(echo $PRETTY_NAME | awk 'FS=" " {print $1;}')
# dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# echo $distro
apt-get update 

# Dependencies
dependencies="python3 \
    python3-tk \
    python3-gpiozero \
    tshark"

# Install dependencies, packages
apt-get -y install $dependencies

# Manually install dependencies that fail on Raspberry Pi OS, else install using pip
if [[ $distro = "Debian" ]]; then
    wget https://files.pythonhosted.org/packages/f4/01/09aac6ea758ca7b7b1b4832c0c39003752ef7b6c1478e6db2f34171db3fe/pycrate-0.7.2.tar.gz
    tar -xzf pycrate-0.7.2.tar.gz
    cd pycrate-0.7.2
    python3 setup.py install
    cd ../
    rm -rf pycrate-0.7.2 pycrate-0.7.2.tar.gz
else 
    pip3 install pycrate
fi
