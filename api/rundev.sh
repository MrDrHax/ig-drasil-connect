#!/bin/bash

source .env
uvicorn main:app --host $HOST --port $PORT --reload