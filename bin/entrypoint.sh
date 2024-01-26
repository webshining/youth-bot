#!/bin/sh

nohup gunicorn -w 4 -b 0.0.0.0:4000 -k uvicorn.workers.UvicornWorker --forwarded-allow-ips=* server:app  &
python main.py