#!/bin/bash

set -e

# Find Distro
source /etc/os-release
distro=$(echo $PRETTY_NAME | awk 'FS=" " {print $1;}')

# System dependencies
sudo apt-get update

dependencies="python3 \
    python3-venv \
    python3-tk \
    python3-gpiozero \
    tshark"

sudo apt-get -y install $dependencies

# Create a venv at the repo root and install Python packages into it
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REPO_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"
VENV_DIR="$REPO_ROOT/.venv"

python3 -m venv --system-site-packages "$VENV_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
pip install --upgrade pip

# Manually install dependencies that fail on Raspberry Pi OS, else install using pip
if [[ $distro = "Debian" ]]; then
    wget https://files.pythonhosted.org/packages/f4/01/09aac6ea758ca7b7b1b4832c0c39003752ef7b6c1478e6db2f34171db3fe/pycrate-0.7.2.tar.gz
    tar -xzf pycrate-0.7.2.tar.gz
    cd pycrate-0.7.2
    python3 setup.py install
    cd ../
    rm -rf pycrate-0.7.2 pycrate-0.7.2.tar.gz
else
    sudo apt-get -y install python3-pip
    pip3 install pycrate
fi

# Install the j2735_202409 package (pulls pycrate as a transitive dependency)
pip install git+https://github.com/usdot-fhwa-stol/j2735_202409.git

echo "Virtual environment ready at $VENV_DIR"
echo "Activate with: source $VENV_DIR/bin/activate"
