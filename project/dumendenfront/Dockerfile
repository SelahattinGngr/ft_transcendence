# Node.js'in resmi imajını kullanıyoruz
FROM node

# Çalışma dizinini belirliyoruz
WORKDIR /app

# package.json ve package-lock.json dosyalarını çalışma dizinine kopyalıyoruz
COPY . ./

# Gerekli Node.js bağımlılıklarını yüklüyoruz
RUN npm install

# Uygulama dosyalarını çalışma dizinine kopyalıyoruz
COPY . .

# Uygulama 3000 portunda çalışacaksa (örneğin)
EXPOSE 3000

# Uygulama başlatma komutunu belirliyoruz (örneğin, `npm start`)
CMD ["npm", "run", "dev"]
