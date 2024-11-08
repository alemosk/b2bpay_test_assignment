#!/bin/bash

# python manage.py collectstatic --no-input

bash ./deployment/wsgi/wait-for-db.sh

# run tests (only applicable for test assigment)
pytest

# migrations
alembic upgrade head

gunicorn b2bpay.config.wsgi:application --bind 0.0.0.0:8080 --preload --timeout 90 -w 2
