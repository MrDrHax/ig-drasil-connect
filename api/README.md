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

## Setup

1. Clone the repository.
2. Run the `setup.sh` script to set up the Python virtual environment and install dependencies.
3. For developing, clone the .example.env file and name it as .dev.env
4. Run the application with `./rundev.sh`.

## Usage

Once the application is running, you can interact with it through its API endpoints. Each app has its own set of endpoints, defined in its endpoints.py file.