# AutoSev - Termux Otomatik Flask Kurulum

Termux uygulamanızda Flask projelerini otomatik olarak kuran ve çalıştıran script.

## 🚀 Tek Komutla Kurulum

Termux'ta şu komutu çalıştır:

```bash
curl -sL https://raw.githubusercontent.com/seghobs/autosev/main/calistir.sh | bash
```

## 📦 Ne Yapar?

Script otomatik olarak:

1. ✅ Termux paketlerini günceller
2. ✅ Python, Git ve Termux API'yi kurar
3. ✅ **Wake lock** alır (telefon kilitli olsa bile çalışır!)
4. ✅ Flask ve requests paketlerini yükler
5. ✅ [kntrl](https://github.com/seghobs/kntrl) projesini indirir
6. ✅ [isimaly](https://github.com/seghobs/isimaly) projesini indirir
7. ✅ Tüm dosyalara gerekli izinleri verir (chmod 777)
8. ✅ Her iki Flask uygulamasını arka planda başlatır
9. ✅ Otomatik başlatma scripti oluşturur (Termux açılınca otomatik çalışır)

## 📁 Klasör Yapısı

```
$HOME/flask_apps/
├── kntrl/
│   ├── flask_app.py
│   └── kntrl.log
└── isimaly/
    ├── flask_app.py
    └── isimaly.log
```

## 🔍 Sunucu Durumunu Kontrol

```bash
# Kntrl logları
tail -f ~/flask_apps/kntrl/kntrl.log

# İsimaly logları
tail -f ~/flask_apps/isimaly/isimaly.log
```

## 🛑 Sunucuları Durdur

```bash
pkill -f flask_app.py
```

## 🔄 Projeleri Güncelle ve Yeniden Başlat

Aynı komutu tekrar çalıştır:

```bash
curl -sL https://raw.githubusercontent.com/seghobs/autosev/main/calistir.sh | bash
```

## 📝 Manuel Kurulum

Eğer manuel olarak yapmak istersen:

```bash
# Script'i indir
curl -O https://raw.githubusercontent.com/seghobs/autosev/main/calistir.sh

# İzin ver
chmod +x calistir.sh

# Çalıştır
./calistir.sh
```

## ⚠️ Gereksinimler

- Android cihaz
- Termux uygulaması
- İnternet bağlantısı

## 🔒 Telefon Kilitleme Sorunu Çözümü

Script otomatik olarak **wake lock** alır, böylece:

✅ Telefon kilitli olsa bile sunucular çalışmaya devam eder
✅ Termux arka planda durmaz
✅ Flask uygulamaları kesintisiz çalışır

### 🚀 Termux:Boot ile Tam Otomatik (Opsiyonel)

Telefon açılınca otomatik başlaması için:

1. Play Store'dan **Termux:Boot** uygulamasını yükle
2. Uygulamayı bir kez aç (izin vermek için)
3. Telefonu yeniden başlat

**Artık telefon açılınca sunucular otomatik başlar!**

### Wake Lock'u Kaldırma

Eğer pil tasarrufu istersen:

```bash
termux-wake-unlock
```

## 🆘 Sorun Giderme

**Hata: Permission denied**
```bash
chmod +x calistir.sh
```

**Hata: Command not found**
```bash
pkg install curl
```

**Flask çalışmıyor**
```bash
# Logları kontrol et
tail ~/flask_apps/kntrl/kntrl.log
tail ~/flask_apps/isimaly/isimaly.log
```

---

**Made with ❤️ for Termux**
