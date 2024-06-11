#!/bin/bash

source .dev.env
uvicorn main:app --host localhost --port 8080
