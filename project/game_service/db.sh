#!/bin/bash

# PostgreSQL hizmetini başlat
service postgresql start

# PostgreSQL veritabanını ve kullanıcısını oluştur
echo "Creating database and user..."

su postgres -c "psql -c \"CREATE DATABASE $GAME_DB_NAME;\""
su postgres -c "psql -c \"CREATE USER $GAME_USER_NAME WITH PASSWORD '$GAME_USER_PASS';\""
su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $GAME_DB_NAME TO $GAME_USER_NAME;\""

# Veritabanı yapılandırması tamamlandıktan sonra
# Django uygulamasını başlatmak için bir komut ekle
# Python uygulamanı başlat
exec "$@"
