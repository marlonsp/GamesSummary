#!/bin/bash

# Nome do arquivo CSV que precisa ser verificado
CSV_FILE="data/games_data.csv"

# Caminho do script Python FastAPI
PYTHON_SCRIPT="src/main.py"

# Verifica se o ambiente virtual já existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativa o ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instala as dependências do requirements.txt
echo "Instalando dependências do requirements.txt..."
pip install -r requirements.txt

# Verifica se o arquivo CSV existe
if [ -f "$CSV_FILE" ]; then
    echo "Arquivo CSV encontrado: $CSV_FILE"
    
    # Executa o script Python com FastAPI
    echo "Executando o script Python $PYTHON_SCRIPT..."
    uvicorn $PYTHON_SCRIPT:app --reload
else
    echo "Arquivo CSV não encontrado: $CSV_FILE"
    echo "Por favor, verifique se o arquivo CSV está no diretório correto."
fi

# Desativa o ambiente virtual
echo "Desativando ambiente virtual..."
deactivate
