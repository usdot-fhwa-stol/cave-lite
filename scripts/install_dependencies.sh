#!/bin/sh

# Declarations, may be needed later
# distro=$(cat /etc/lsb-release | grep DISTRIB_CODENAME |  tr -d "DISTRIB_CODENAME=")
# dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

apt-get update 

# Dependencies
dependencies="python3 \
    python3-tk \
    python3-gpiozero \
    tshark"

# Install dependencies, packages
apt-get -y install $dependencies

# Manually install dependencies that fail on Raspberry Pi OS
wget https://files.pythonhosted.org/packages/f4/01/09aac6ea758ca7b7b1b4832c0c39003752ef7b6c1478e6db2f34171db3fe/pycrate-0.7.2.tar.gz
tar -xzf pycrate-0.7.2.tar.gz
cd pycrate-0.7.2
python3 setup.py install
cd ../
rm -rf pycrate-0.7.2 pycrate-0.7.2.tar.gz

