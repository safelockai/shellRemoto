#!/bin/bash

# Atualizar pacotes
pkg update && pkg upgrade -y

# Instalar Python
pkg install python -y

# Instalar pip (gerenciador de pacotes Python)
pkg install python-pip -y

# Instalar a biblioteca requests para Python
pip install requests

# Instalar Git (opcional, se precisar clonar repositórios)
pkg install git -y

echo "Todos os pré-requisitos foram instalados com sucesso!"
