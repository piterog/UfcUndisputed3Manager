#!/bin/sh
# Espera o PostgreSQL iniciar
echo "Waiting for PostgreSQL..."
until pg_isready -h db -p 5432 -U userufcu3 -d ufcu3managerdb; do
  echo "Aguardando o banco de dados..."
  sleep 1
done
echo "PostgreSQL started"

# Verifica se as tabelas existem, mas NÃO recria o banco
python - <<EOF
from sqlalchemy import create_engine, inspect
import os

db_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
engine = create_engine(db_uri)
inspector = inspect(engine)
tables = inspector.get_table_names()

if not tables:
    print("Banco de dados vazio, inicializando estrutura...")
    import init_db
    init_db.init_database()
else:
    print("Estrutura do banco de dados já existe, mantendo dados...")
EOF

# Inicia a aplicação Flask
flask run --host=0.0.0.0
