#!/bin/bash
set -e

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
