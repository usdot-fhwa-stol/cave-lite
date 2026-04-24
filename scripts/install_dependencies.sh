#!/bin/bash

set -e

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

# Install the j2735_202409 package (pulls pycrate as a transitive dependency)
pip install git+https://github.com/usdot-fhwa-stol/j2735_202409.git

echo "Virtual environment ready at $VENV_DIR"
echo "Activate with: source $VENV_DIR/bin/activate"
