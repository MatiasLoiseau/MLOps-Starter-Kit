# MLOps-Started-Kit
This repository contains a practical project developed as part of the MLOps certification program at ITBA. It provides a basic yet functional implementation of an MLOps architecture designed to automate the complete workflow of a machine learning project, from data management to model deployment.

## Instalación de env conda
```bash
conda create -n mlops-env python=3.12
conda activate mlops-env
pip install mlflow
conda install -c conda-forge psycopg2
```
## Definición de variables de entorno

Desde carpeta del repo

```bash
# Seteo de variables
export REPO_FOLDER=${PWD}
set -o allexport && source .env && set +o allexport

# Verificarlo
echo $postgres_data_folder
```

## PSQL DB

### Bajar imagen
```bash
docker pull postgres
```

### Correr imagen
```bash
docker run -d \
    --name mlops-postgres \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v $postgres_data_folder:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres
```

### Verificar funcionamiento, y manejo del contenedor
```bash
docker ps

docker ps -a

docker exec -it mlops-postgres /bin/bash

root@08487b094f8a$  psql -U postgres

postgres   exit

root@08487b094f8a$  exit
```

Instalar psql para acceder más rápido:
```bash
sudo apt install postgresql-client-16
export PGPASSWORD=$POSTGRES_PASSWORD 
psql -U postgres -h localhost -p 5432
```

#### Create MLFLOW DB

```sql
CREATE DATABASE mlflow_db;
CREATE USER mlflow_user WITH ENCRYPTED PASSWORD 'mlflow';
GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;
```

#### (optional) install Dbeaver

https://dbeaver.io/download/

```bash
flatpak install flathub io.dbeaver.DBeaverCommunity
```

## Run MLFlow server

Remember from repository path:
```bash
conda activate mlops-env
export REPO_FOLDER=${PWD}
set -o allexport && source .env && set +o allexport
```

And then:

```bash
mlflow server --backend-store-uri postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST/$MLFLOW_POSTGRES_DB --default-artifact-root $MLFLOW_ARTIFACTS_PATH -h 0.0.0.0 -p 8002
```

Abrir browser en http://localhost:8002/

## Install Airbyte Linux

Follow the instructions:

https://docs.airbyte.com/using-airbyte/getting-started/oss-quickstart


#### Troubleshouting ubuntu:

Airbyte uses docker and need non-sudo

```bash
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```
