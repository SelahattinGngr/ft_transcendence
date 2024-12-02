#!/bin/bash

# PostgreSQL hizmetini başlat
service postgresql start

# PostgreSQL veritabanını ve kullanıcısını oluştur
echo "Creating database and user..."
echo $CHAT_DB_NAME
echo $CHAT_USER_PASS
echo $CHAT_USER_NAME

su postgres -c "psql -c \"CREATE DATABASE $CHAT_DB_NAME;\""
su postgres -c "psql -c \"CREATE USER $CHAT_USER_NAME WITH PASSWORD '$CHAT_USER_PASS';\""
su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $CHAT_DB_NAME TO $CHAT_USER_NAME;\""

# Veritabanı yapılandırması tamamlandıktan sonra
# Django uygulamasını başlatmak için bir komut ekle
# Python uygulamanı başlat
exec "$@"
