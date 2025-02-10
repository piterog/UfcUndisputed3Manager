FROM python:3.9-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código fonte
COPY . .

# Garante que o Python encontre os módulos
ENV PYTHONPATH="${PYTHONPATH}:/app"

COPY wait-for-db.sh .
RUN chmod +x wait-for-db.sh

# Comando para iniciar
CMD ["./wait-for-db.sh"]
