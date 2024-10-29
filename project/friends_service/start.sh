#!/bin/bash

# PostgreSQL'i başlat
/app/friends_service/db.sh &

# PostgreSQL'in başlatılmasını beklemek için biraz zaman tanı
sleep 5

# Auth servisini başlat
cd /app/friends_service
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000 &

# Container'ı çalışır durumda tutmak için
tail -f /dev/null
