#!/bin/bash  

# Check Python version
ret=`python -c 'import sys; print("%i" % (sys.version_info.major))'`

if [ $ret -eq 3 ]; then
    v=true
    printf "\n****************************\nPython version is 3"
else
    v=false
    printf "\n****************************\nPython version must be >= 3.0.0"
    
    ret=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
    if [ $ret -eq 3 ]; then
        printf "\n****************************\nCreating a temporary alias for python3"
        alias python=python3
    else
        printf "\n****************************\nInstalling Python3"
        sudo apt update
        sudo apt install -y python3 python3-dev python3-venv
        sudo apt-get update
        sudo apt-get install --yes python3-distutils

        alias python=python3
    fi
fi

# Install Pip
pipinstalled=which pip | grep -o pip > /dev/null #&&  printf 0 || printf 1
if [[ pipinstalled -eq 1 ]]; then
    printf "\n****************************\nInstalling pip..."
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
else
    printf "\n****************************\nPip detected."
fi

printf "\n****************************\nInstalando dependências..."  
pip install -r requirements.txt

printf "\n****************************\nVamos começar!!!\n****************************\n"
python simulation.py
