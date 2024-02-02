#!/bin/sh

# exit on errors
set -e

# Declarations, may be needed later
# distro=$(cat /etc/lsb-release | grep DISTRIB_CODENAME |  tr -d "DISTRIB_CODENAME=")
# dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

apt-get update 

# Dependencies
dependencies="python3 \
    python3-pip \
    python3-tk"

# Required python packages
python_packages="pycrate \
    gpiozero"

# Install dependencies, packages
apt-get install -y $dependencies
pip3 install $python_packages
