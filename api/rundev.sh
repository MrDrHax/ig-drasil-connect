#!/bin/bash

source .dev.env
uvicorn main:app --host $HOST --port $PORT --reload