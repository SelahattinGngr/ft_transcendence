// Süreli veri kaydetme fonksiyonu
export function setTemporaryData(key, value, minutes) {
  const expirationTime = new Date().getTime() + minutes * 60 * 1000;
  const data = {
    value: value,
    expiresAt: expirationTime,
  };
  localStorage.setItem(key, JSON.stringify(data));
}

// Veriyi okuma fonksiyonu
export function getTemporaryData(key) {
  const data = localStorage.getItem(key);
  if (!data) return null;

  const item = JSON.parse(data);
  const now = new Date().getTime();

  if (now > item.expiresAt) {
    // Süre dolmuşsa veriyi sil
    localStorage.removeItem(key);
    return null;
  }

  return item.value;
}

// Veriyi silme fonksiyonu
export function removeTemporaryData(key) {
  localStorage.removeItem(key);
}
