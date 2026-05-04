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
    wget https://files.pythonhosted.org/packages/42/70/64a5b11e831dab532b4b61e684c5807a68daeb93b2bd4853975acaaf968e/pycrate-0.7.11.tar.gz
    tar -xzf pycrate-0.7.11.tar.gz
    cd pycrate-0.7.11
    python3 setup.py install
    cd ../
    rm -rf pycrate-0.7.11 pycrate-0.7.11.tar.gz
else
    pip3 install pycrate>=0.7.11
fi

# Install the j2735_202409 package (pulls pycrate as a transitive dependency)
pip install git+https://github.com/usdot-fhwa-stol/j2735_202409.git

echo "Virtual environment ready at $VENV_DIR"
echo "Activate with: source $VENV_DIR/bin/activate"
