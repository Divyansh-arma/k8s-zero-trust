#!/bin/bash
cd /var/app/current
source /var/app/venv/*/bin/activate
python application.py db upgrade