# Ig-drasil connect backend

This is a FastAPI application with the following structure:

- main.py: The entry point of the application.
- db.py: Sets up a global database pool.
- config.py: Loads environment variables and sets up the application configuration.
- requirements.txt: Lists the Python packages that the application depends on.
- setup.sh: A bash script that sets up a Python virtual environment and installs dependencies.

The application is divided into several apps, each with its own directory:

- dashboard
- lists
- summary
- actions
- extras

Each app has the following files:

- crud.py: Defines the CRUD operations for the app.
- models.py: Defines the data models for the app.
- endpoints.py: Defines the API endpoints for the app.

> Note: you can nor run by using `python -m main.py` (the -m is **VERY** necessary) 

## Setup

1. Clone the repository.
2. Run the `setup.sh` script to set up the Python virtual environment and install dependencies.
3. For developing, clone the .example.env file and name it as .dev.env
4. Run the application with `./rundev.sh`.

## For Windows 
1. Clone the repository.
2. In the `setup.sh`replace `python3 -m venv connectEnv` for `python -m venv connectEnv`
3. Paste `.\connectEnv\Scripts\Activate.ps1` in powershell
4. Follow the last two steps of `setup.sh`
5. Run the application using `uvicorn main:app --host $HOST --port $PORT --reload` replacing the values with the dotenv keys.

## Usage

Once the application is running, you can interact with it through its API endpoints. Each app has its own set of endpoints, defined in its endpoints.py file.

## Iniciar contenedores

1. Descargar Docker Desktop 
2. Verificar la Version de Docker Compose (prueba los siguientes comandos)

        docker compose version = v1
        docker-compose version = v2

- Limpiar docker 

        docker system prune -f
        docker builder prune 

3. Ejecutar docker 

        docker compose up -d


# Fuentes

https://www.mongodb.com/docs/manual/core/schema-validation/specify-json-schema/ 
https://www.mongodb.com/docs/manual/reference/operator/query/jsonSchema/#mongodb-query-op.-jsonSchema
