#!/bin/bash

# PostgreSQL hizmetini başlat
service postgresql start

# PostgreSQL veritabanını ve kullanıcısını oluştur
echo "Creating database and user..."

su postgres -c "psql -c \"CREATE DATABASE $USER_DB_NAME;\""
su postgres -c "psql -c \"CREATE USER $USER_USER_NAME WITH PASSWORD '$USER_USER_PASS';\""
su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $USER_DB_NAME TO $USER_USER_NAME;\""

# Veritabanı yapılandırması tamamlandıktan sonra
# Django uygulamasını başlatmak için bir komut ekle
# Python uygulamanı başlat
exec "$@"
