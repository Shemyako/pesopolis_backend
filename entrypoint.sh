#!/usr/bin/env bash

gunicorn src.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --timeout 120 --bind 0.0.0.0:80
