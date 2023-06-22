#!/bin/bash
while true; do
    python3 manage.py collectstatic
    python3 manage.py runserver localhost:8000
    echo "Server crashed, waiting for changes..."
    sleep 2
done
