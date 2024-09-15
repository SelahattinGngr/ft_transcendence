#!/bin/bash

# PostgreSQL'i başlat
/app/auth_service/db.sh &

# PostgreSQL'in başlatılmasını beklemek için biraz zaman tanı
sleep 5

# Auth servisini başlat
cd /app/auth_service
python3 manage.py makemigrations
python3 manage.py migrate
python3 src/apps.py &

# Container'ı çalışır durumda tutmak için
tail -f /dev/null
