#!/bin/bash  

# Check Python version
ret=`python -c 'import sys; print("%i" % (sys.version_info.major))'`
if [ $ret -eq 3 ]; then
    v=true
    echo "Python version is 3"
else
    v=false
    echo "Python version must be >= 3.0.0"
    
    version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
    echo $version
    if [[ -z "$version" ]]
        alias python=python3
    then
        echo "Installing Python3"
        apt update
        apt install -y python3 python3-dev python3-venv
        apt-get update
        apt-get install --yes python3-distutils

        alias python=python3
    fi
fi

# Install Pip
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py

echo "Instalando dependências..."  
pip install -r requirements.txt

echo "Vamos começar!!!"
{ # try
    python simulation.py &&
    #save your output
} || { # catch
    python3 simulation.py
    # save log for exception 
}
