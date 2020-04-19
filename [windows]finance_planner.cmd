@echo off

echo "Rapidinho...preciso instalar umas coisas aqui..."
python get-pip.py

echo "Mais um momento...instalando dependências..."  
pip install -r requirements.txt

echo "Vamos começar!!!"
python simulation.py
