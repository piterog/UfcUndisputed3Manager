#!/bin/sh

# Espera o PostgreSQL iniciar
echo "Waiting for PostgreSQL..."
until pg_isready -h db -p 5432 -U postgres; do
  echo "Aguardando o banco de dados..."
  sleep 1
done
echo "PostgreSQL started"

# Inicializa o banco de dados
python init_db.py

# Inicia a aplicação Flask
flask run --host=0.0.0.0
