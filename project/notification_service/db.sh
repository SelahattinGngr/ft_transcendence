#!/bin/bash

# PostgreSQL hizmetini başlat
service postgresql start

# PostgreSQL veritabanını ve kullanıcısını oluştur
echo "Creating database and user..."
echo $NOTIFICATION_DB_NAME
echo $NOTIFICATION_USER_PASS
echo $NOTIFICATION_USER_NAME

su postgres -c "psql -c \"CREATE DATABASE $NOTIFICATION_DB_NAME;\""
su postgres -c "psql -c \"CREATE USER $NOTIFICATION_USER_NAME WITH PASSWORD '$NOTIFICATION_USER_PASS';\""
su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $NOTIFICATION_DB_NAME TO $NOTIFICATION_USER_NAME;\""

# Veritabanı yapılandırması tamamlandıktan sonra
# Django uygulamasını başlatmak için bir komut ekle
# Python uygulamanı başlat
exec "$@"
