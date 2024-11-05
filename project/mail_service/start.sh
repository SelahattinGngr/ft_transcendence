#!/bin/bash

# auth servisini başlat
cd /app/mail_service

python3 manage.py runserver 0.0.0.0:8000 &

# container'ı çalışır durumda tutmak için
tail -f /dev/null