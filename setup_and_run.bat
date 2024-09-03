@echo off

REM Nome do arquivo CSV que precisa ser verificado
set CSV_FILE=data\games_data.csv

REM Caminho do script Python FastAPI
set PYTHON_SCRIPT=app.py

REM Verifica se o ambiente virtual já existe
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativa o ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate

REM Instala as dependências do requirements.txt
echo Instalando dependências do requirements.txt...
pip install -r requirements.txt

REM Verifica se o arquivo CSV existe
if exist "%CSV_FILE%" (
    echo Arquivo CSV encontrado: %CSV_FILE%
    
    REM Executa o script Python com FastAPI
    echo Executando o script Python %PYTHON_SCRIPT%...
    python %PYTHON_SCRIPT%
) else (
    echo Arquivo CSV não encontrado: %CSV_FILE%
    echo Por favor, verifique se o arquivo CSV está no diretório correto.
)

REM Desativa o ambiente virtual
echo Desativando ambiente virtual...
deactivate
