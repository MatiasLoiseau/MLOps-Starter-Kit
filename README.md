# MLOps Starter Kit

This repository contains a practical project developed as part of the MLOps certification program at ITBA. It demonstrates a basic yet functional implementation of an MLOps architecture, automating the entire machine learning workflow, from data management to model deployment.

---

## Installation Guide

### 1. Create the Conda Environment

```bash
conda create -n mlops-env python=3.12
conda activate mlops-env
pip install mlflow
conda install -c conda-forge psycopg2
```

### 2. Set Environment Variables

From the repository's root folder:

```bash
export REPO_FOLDER=${PWD}
set -o allexport && source .env && set +o allexport
echo $postgres_data_folder
```
---

## Setting Up PostgreSQL

### 1. Pull the Docker Image

```bash
docker pull postgres
```

### 2. Run the PostgreSQL Container

```bash
docker run -d \
    --name mlops-postgres \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v $postgres_data_folder:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres
```

### 3. Verify and Manage the Container

Common Docker commands:

```bash
docker ps
docker ps -a
docker exec -it mlops-postgres /bin/bash
```
Access PostgreSQL inside the container:

```bash
psql -U postgres
postgres=# \q
exit
```

### 4. Install PostgreSQL Client (Optional)

```bash
sudo apt install postgresql-client-16
export PGPASSWORD=$POSTGRES_PASSWORD
psql -U postgres -h localhost -p 5432
```

### 5. Create the MLFlow Database

Run these SQL commands to set up the database:

```sql
CREATE DATABASE mlflow_db;
CREATE USER mlflow_user WITH ENCRYPTED PASSWORD 'mlflow';
GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;
```
---

## Running the MLFlow Server

### 1. Activate Conda and Set Environment Variables

```bash
conda activate mlops-env
export REPO_FOLDER=${PWD}
set -o allexport && source .env && set +o allexport
```

### 2. Start the MLFlow Server

```bash
mlflow server \
    --backend-store-uri postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST/$MLFLOW_POSTGRES_DB \
    --default-artifact-root $MLFLOW_ARTIFACTS_PATH \
    -h 0.0.0.0 \
    -p 8002
```

### 3. Access MLFlow

Open your browser and navigate to: [http://localhost:8002/](http://localhost:8002/)

---

## Installing Airbyte

### 1. Install Airbyte

Follow the [Airbyte Quickstart Guide](https://docs.airbyte.com/using-airbyte/getting-started/oss-quickstart).

### 2. Grant Non-Sudo Access to Docker

```bash
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

### 3. Start Airbyte and Add Sources

Start Airbyte and navigate to [http://localhost:8000/](http://localhost:8000/). Add the following sources:

- `https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/peliculas_0.csv`
- `https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/usuarios_0.csv`
- `https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/scores_0.csv`

### 4. Set Up the Destination

Grant permissions to the Airbyte user:

```sql
CREATE DATABASE mlops;
CREATE USER "yourmail@gmail.com" WITH ENCRYPTED PASSWORD 'airbyte';
GRANT ALL PRIVILEGES ON DATABASE mlops TO "yourmail@gmail.com";
GRANT ALL ON SCHEMA public TO "yourmail@gmail.com";
ALTER DATABASE mlops OWNER TO "yourmail@gmail.com";
```
---

## Setting Up DBT

### 1. Install DBT and Initialize the Project

```bash
pip install dbt-postgres
dbt init db_postgres
```

### 2. Configure DBT

Follow the prompts during initialization:

- Host: `localhost`
- Port: `5432`
- User: `yourmail@gmail.com`
- Database: `mlops`
- Schema: `target`

### 3. Create and Run Models

1. Add SQL transformations in `db_postgres/models`.
2. Create a `schema.yml` file.
3. Configure `dbt_project.yml`.
4. Test DBT with `dbt debug`, then execute with `dbt run`.

Go to [this commit](https://github.com/MatiasLoiseau/MLOps-Started-Kit/commit/3b67c813e1c631899660e92711cd78815c2903ef) to configure steps 1 to 3.

---

## Optional Tools

### DBeaver Installation (Optional)

Install DBeaver for database visualization:

```bash
flatpak install flathub io.dbeaver.DBeaverCommunity
```     

---