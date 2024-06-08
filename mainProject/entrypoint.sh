#!/bin/bash

echo "Apply DB Migrations" 
python3 manage.py makemigrations
python3 manage.py migrate 


exec "$@"