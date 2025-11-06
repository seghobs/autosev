# 🚀 Termux Panel - Modern Web Yönetim Paneli

Flask + Bootstrap ile geliştirilmiş, **Android Termux** için özel tasarlanmış modern web yönetim arayüzü.

## ✨ Özellikler

### 📦 Proje Yönetimi
- GitHub projelerini otomatik indirme ve kurma
- Flask ve Django projelerini otomatik algılama
- Projeleri tek tıkla başlatma
- Port bilgilerini otomatik tespit etme
- Proje linklerine direk erişim (örn: http://127.0.0.1:9000)
- Projeleri kökten silme

### 🔧 Paket Yönetimi
- Kurulu Python paketlerini görüntüleme
- Yeni paket kurma (pip install)
- Paket kaldırma (pip uninstall)
- Arama ve filtreleme

### 🖥️ Proses Yönetimi
- Çalışan Python/Flask/Django proseslerini görme
- Proses detaylarını görüntüleme (PID, port, başlatma zamanı)
- Prosesleri durdurma
- Port bilgilerine göre linkleri görme

### 🌐 Sunucu Yönetimi
- Aktif Flask/Django sunucularını listeleme
- Sunucu linklerine direk erişim
- Gerçek zamanlı sunucu durumu

### 🎨 Modern Arayüz
- Bootstrap 5 koyu tema
- Tam responsive tasarım (mobil uyumlu)
- Modern ve şık görünüm
- Telefon dostu kontroller

### ⚡ Otomatik Başlatma
- Termux açılışında otomatik başlat
- Tarayıcı otomatik açılır
- Arka planda çalışır
- Tek kurulum ile hazır!

## 📱 Termux Kurulumu

### 1. Gerekli Paketleri Kur
```bash
pkg update && pkg upgrade
pkg install python git
```

### 2. Projeyi İndir
```bash
cd ~
git clone https://github.com/KULLANICI_ADINIZ/termux-panel.git
cd termux-panel
```

### 3. Python Paketlerini Kur
```bash
pip install -r requirements.txt
```

### 4. Kurulum Scriptini Çalıştır (Otomatik Başlatma)
```bash
chmod +x install_termux.sh
./install_termux.sh
```

**✨ Kurulum scripti:**
- Python paketlerini kurar
- Otomatik başlatmayı ayarlar
- Termux her açıldığında panel otomatik başlar!

### 5. Termux'u Yeniden Başlat
Termux'u kapatып açın - Panel otomatik başlayacak ve tarayıcı açılacak!

**Otomatik Başlatmayı Kaldırmak:**
```bash
chmod +x disable_autostart.sh
./disable_autostart.sh
```

**Manuel Başlatma:**
```bash
python app.py
```

**Tarayıcıda Aç:**
```bash
termux-open-url http://127.0.0.1:5000
```

Veya:
```
http://127.0.0.1:5000
```

## 🎯 Kullanım

### GitHub Projesini İndirme ve Çalıştırma
1. **Projeler** sayfasına git
2. GitHub repo URL'sini yapıştır (örn: `https://github.com/user/repo.git`)
3. **İndir ve Yükle** butonuna bas
4. Proje otomatik indirilir ve `chmod 777` izinleri verilir
5. Proje kartında **Başlat** butonuna basarak çalıştır
6. **Önemli:** Proje yeni bir terminal penceresinde çalışır
   - Terminal açık kaldığı sürece proje çalışmaya devam eder
   - Durdurmak için terminal penceresini kapatın veya **Prosesler** sayfasından durdurun

### Paket Yönetimi
1. **Paketler** sayfasına git
2. Yeni paket kurmak için paket adını yaz ve **Kur** butonuna bas
3. Mevcut paketleri görmek için listeyi incele
4. Paket kaldırmak için **Kaldır** butonuna bas

### Çalışan Prosesleri Görme
1. **Prosesler** sayfasına git
2. Tüm çalışan Python/Flask/Django proseslerini gör
3. Port bilgisi varsa link üzerinden direk erişim sağla
4. **Durdur** butonu ile prosesi sonlandır

### Sunucu Linkleri
1. **Sunucular** sayfasına git
2. Aktif tüm Flask/Django sunucularını gör
3. Port bazlı linkler otomatik oluşturulur
4. **Aç** butonu ile yeni sekmede aç

## 🔧 Yapılandırma

### Port Değiştirme
`app.py` dosyasının son satırını düzenleyin:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Projeler Dizini
Varsayılan olarak projeler `termux-panel/projects/` dizinine indirilir.

## 📋 Sistem Gereksinimleri

- **Android** (Termux uygulaması)
- **Python** 3.8+
- **Git** (proje indirme için)
- En az 100MB boş alan

## 🔒 Güvenlik Notları

⚠️ **Önemli**: Bu panel local (127.0.0.1) üzerinde çalışır. Dışarıdan erişim için ekstra güvenlik önlemleri alınmalıdır.

- Production ortamında `debug=False` yapın
- Güvenli bir `SECRET_KEY` kullanın
- Gerekirse authentication ekleyin

## 🐛 Sorun Giderme

### Port zaten kullanımda
```bash
# Çalışan uygulamayı bulun
ps aux | grep python
# PID ile sonlandırın
kill -9 PID_NUMARASI
```

### Permission denied hatası
```bash
chmod +x app.py
```

### Paket kurulum hatası
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Otomatik başlatmayı durdurmak
```bash
# Devre dışı bırakmak için
chmod +x disable_autostart.sh
./disable_autostart.sh

# Veya manuel olarak
sed -i '/# Termux Panel Auto-Start/,/# End Termux Panel/d' ~/.bashrc
```

### Panel'i durdurmak
```bash
# PID'yi bul
ps aux | grep "app.py"

# Durdur
kill PID_NUMARASI

# Veya hepsini durdur
pkill -f "python.*app.py"
```

## 📝 Lisans

MIT License - Ücretsiz kullanabilirsiniz.

## 🤝 Katkıda Bulunma

Pull request'ler kabul edilir! Büyük değişiklikler için önce issue açın.

## 💡 İpuçları

- Panel otomatik 5-10 saniyede bir yenilenir
- GitHub private repo'lar için token gerekebilir
- Projeler `flask_app.py`, `app.py`, `main.py`, `run.py` veya `manage.py` dosyalarından otomatik başlatılır
- Port bilgisi koddan otomatik çıkarılır

## 📞 Destek

Sorun yaşıyorsanız GitHub Issues kullanın.

---

**Termux Panel** ile Android cihazınızda profesyonel Python geliştirme! 🎉
