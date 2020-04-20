@echo off

goto :DOES_PYTHON_EXIST

:DOES_PYTHON_EXIST
python -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
python -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
pause
goto :EOF

:PYTHON_DOES_NOT_EXIST
echo Precisamos instalar o Python!
echo Na janela de instalacao, selecione para adicionar variáveis ao PATH!
echo Na janela de instalacao, selecione para adicionar variáveis ao PATH!
echo Na janela de instalacao, selecione para adicionar variáveis ao PATH!
echo . & echo.PRIMEIRO...
echo                  ^|
echo                  ^|
echo                  ^|
echo                  V
echo                  _
echo  -------------^> ^|_^| Add Python 3.X to PATH. ^<---------------
echo                  ^^
echo                  ^|
echo                  ^|
echo                  ^|
echo                                   ...DEPOIS "Install NOW"
echo . & echo.Pressione barra de ESPACO para iniciar instalacao. . .
pause >NUL
start "" "dependencies\python-3.8.2-amd64.exe"
echo .................................................................
echo Pressione barra de ESPACO para continuar. . .
pause >NUL
echo .
FOR /f %%p in ('where python') do SET PYTHONPATH=%%p
ECHO %PYTHONPATH% & echo..
goto :PYTHON_IS_THREE

:PYTHON_DOES_EXIST
:: This will retrieve Python 3.8.0 for example.
for /f "delims=" %%V in ('python -V') do @set ver=%%V
IF "%ver:~7,1%"=="3" ( goto :PYTHON_IS_THREE 
) ELSE ( goto :PYTHON_DOES_NOT_EXIST 
)

:PYTHON_IS_THREE
echo .................................................................
echo Boa!, %ver% foi instalado...
echo Rapidinho...preciso verificar umas coisas aqui... & echo..
for /f "delims=" %%V in ('pip -V') do @set ver=%%V
IF NOT "%ver:~0,3%"=="pip" ( python get-pip.py 
) ELSE ( echo %ver:~0,10% ja esta instalado! 
)
echo .................................................................
echo Mais um momento...to instalando algumas dependencias... & echo..
pip install -r requirements.txt
echo .................................................................
cls
echo Vamos comecar!!! & echo..
python simulation.py
echo .
echo .
echo .
pause
goto :EOF