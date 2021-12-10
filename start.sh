#!bin/bash
gunicorn3 --workers=3 wsgi:application

