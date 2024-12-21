# MLOps Starter Kit

This repository contains a practical project developed as part of the MLOps certification program at ITBA. It provides a basic yet functional implementation of an MLOps architecture designed to automate the complete workflow of a machine learning project, from data management to model deployment.

## Features
- Environment setup with    conda and pip
- PostgreSQL database setup using Docker
- MLFlow server configuration for tracking machine learning experiments
- Integration with Airbyte for data management

---

## Install basic components

### 1. Create a Conda Environment

```bash
conda create -n mlops-env python=3.12
conda activate mlops-env
pip install mlflow
conda install -c conda-forge psycopg2
```

### 2. Set Environment Variables
From the repository's root folder:

```bash
# Export the repository folder as an environment variable
export REPO_FOLDER=${PWD}

# Load variables from the .env file
set -o allexport && source .env && set +o allexport

# Verify the environment variable
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

```bash
# List running containers
docker ps
# List all containers (including stopped ones)
docker ps -a
# Access the container's shell
docker exec -it mlops-postgres /bin/bash
# Access PostgreSQL from the container's shell
psql -U postgres
# Exit PostgreSQL
postgres=# \q
# Exit the container's shell
root@container-id$ exit
```

### 4. Install PostgreSQL Client (Optional)
For easier access to the database:

```bash
sudo apt install postgresql-client-16
export PGPASSWORD=$POSTGRES_PASSWORD
psql -U postgres -h localhost -p 5432
```

### 5. Create the MLFlow Database
Access the PostgreSQL client and run the following SQL commands:

```sql
CREATE DATABASE mlflow_db;
CREATE USER mlflow_user WITH ENCRYPTED PASSWORD 'mlflow';
GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;
```

---

## Running the MLFlow Server

### 1. Activate the Conda environment and set environment variables:

```bash
conda activate mlops-env
export REPO_FOLDER=${PWD}
set -o allexport && source .env && set +o allexport
```

### 2. Start the MLFlow server:

```bash
mlflow server --backend-store-uri postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST/$MLFLOW_POSTGRES_DB --default-artifact-root $MLFLOW_ARTIFACTS_PATH -h 0.0.0.0 -p 8002
```

### 3. Open MLFlow

Open your browser and navigate to: [http://localhost:8002/](http://localhost:8002/)

---

## Installing Airbyte on Linux

### 1. Follow the Official Instructions
Refer to the official Airbyte documentation for a quickstart guide: [Airbyte Quickstart Guide](https://docs.airbyte.com/using-airbyte/getting-started/oss-quickstart)

### 2. Troubleshooting on Ubuntu
Airbyte uses Docker and requires non-sudo access:

```bash
sudo usermod -aG docker $USER
newgrp docker
# Test the Docker installation
docker run hello-world
```

### 3. Open Airbyte

Check with `docker ps -a` if airbyte is running, then open your browser and navigate to: [http://localhost:8000/](http://localhost:8000/)

---

## Optional Tools

### Install DBeaver (Optional)
DBeaver is a database management tool that can be used to visualize and manage PostgreSQL databases.

#### Installation via Flatpak:

```bash
flatpak install flathub io.dbeaver.DBeaverCommunity
```

---