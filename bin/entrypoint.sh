#!/bin/sh

nohup hypercorn server:app --bind 0.0.0.0:4000 &
python main.py