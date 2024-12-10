Docker'da gereksiz görüntüleri (image), kapsayıcıları (container), hacimleri (volume) ve build cache'leri temizlemek için şu komutları kullanabilirsiniz:

---

### 1. **Tüm Kapsayıcıları Silmek**
Çalışan ve durdurulmuş tüm kapsayıcıları silmek için:
```bash
docker rm -f $(docker ps -aq)
```
- **Açıklama**: `docker ps -aq` tüm kapsayıcıların ID'sini döner. `docker rm -f` ile hepsi zorla silinir.

---

### 2. **Tüm Görüntüleri Silmek**
Tüm Docker imajlarını silmek için:
```bash
docker rmi -f $(docker images -aq)
```
- **Açıklama**: `docker images -aq` tüm görüntülerin ID'sini döner. `docker rmi -f` ile hepsi zorla silinir.

---

### 3. **Tüm Hacimleri Silmek**
Kullanılmayan tüm hacimleri temizlemek için:
```bash
docker volume prune -f
```
- Eğer **tüm** hacimleri silmek isterseniz:
```bash
docker volume rm $(docker volume ls -q)
```
- **Açıklama**: `docker volume ls -q` tüm hacimlerin isimlerini döner. `docker volume rm` ile hepsi silinir.

---

### 4. **Build Cache'lerini Temizlemek**
Docker'ın build cache'ini temizlemek için:
```bash
docker builder prune -a --force
```
- **Açıklama**: `-a` seçeneği tüm build cache'lerini siler.

---

### 5. **Her Şeyi Birlikte Temizlemek**
Bir komutla tüm kullanılmayan nesneleri (ağlar, hacimler, build cache'ler, durdurulmuş kapsayıcılar) temizlemek için:
```bash
docker system prune -a --volumes --force
```
- **`-a`**: Kullanılmayan tüm görüntüleri de temizler.
- **`--volumes`**: Kullanılmayan tüm hacimleri de temizler.

---

### Dikkat Edilmesi Gerekenler
- Bu komutlar **geri dönüşü olmayan** işlemler yapar, bu yüzden önemli verilerinizi ve yapılandırmalarınızı silmeden önce yedeklediğinizden emin olun.
- Hangi nesneleri silmek istediğinizden emin değilseniz, komutları `--dry-run` seçeneği ile çalıştırarak önce nelerin silineceğini görebilirsiniz (bazı komutlarda desteklenir).