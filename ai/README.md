# Ai module for ig-drasil connect 

This document is the AI module to use for end users and agents

## Install dependencies

`pip install -r requrements.txt`

This code does not work on windows!!!!

I am not changing it. 

You might need to install uvicorn directly to run it:

`sudo apt install uvicorn`

Or create a venv https://python.land/virtual-environments/virtualenv

> AI modules will get installed on first time run. This might take a few minutes!!! (it's around 4Gb of data)

## Run program

You can use the vscode debugger, add this `launch.json`


```jsonc
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: from app",
            "type": "debugpy",
            "request": "launch",
            "module": "main"
        },
        {
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--host",
                "localhost",
                "--port",
                "8081",
                "--reload"
            ],
            "jinja": true,
            "envFile": "${workspaceFolder}/.dev.env"
        }
    ]
}
```

Another method is to run uvicorn directly.

`uvicorn main:app --host localhost --port 8081 --reload`

The final method is:

`python -m main.py`

## How to develop

### API endpoints

Since the endpoints in the AI are limited, all of them lie on the `main.py` file.

### LLM and gpt

All LLM stuff is under the `GPT/` folder. 

The session manager is where you can create and prompt sessions. A single instance of the module should be present unless multithreading.

### Parsers

Parsers help get jsons or raw inormation, and turn it into gpt unserstandable prompts. Anythin 