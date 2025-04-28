FROM python:3.9-slim

# Atualizar o pip
RUN pip install --upgrade pip

# Atualizar a lista de pacotes e instalar o netcat (usando netcat-openbsd)
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd

# Definir diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos de requisitos para o container
COPY requirements.txt /app/

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código para o diretório de trabalho do container
COPY . /app/

# Expor a porta 10000 para acesso externo
EXPOSE 10000

# Definir o comando de execução do container (iniciar o servidor FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000", "--reload"]
