#!/data/data/com.termux/files/usr/bin/bash

# Renkli çıktı için
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}  Termux Otomatik Kurulum Başlatılıyor${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"

# Çalışma dizinini al
INSTALL_DIR="$HOME/flask_apps"

echo -e "\n${YELLOW}[1/7] Termux paketleri güncelleniyor...${NC}"
pkg update -y && pkg upgrade -y

echo -e "\n${YELLOW}[2/7] Python, Git ve Termux API kuruluyor...${NC}"
pkg install -y python git termux-api

echo -e "\n${YELLOW}[2.5/7] Wake lock alınıyor (telefon arka planda olsa bile çalışacak)...${NC}"
termux-wake-lock

echo -e "\n${YELLOW}[3/7] Python paketleri kuruluyor...${NC}"
pip install --upgrade pip
pip install flask requests

echo -e "\n${YELLOW}[4/7] Projeler indiriliyor...${NC}"
# Ana dizini oluştur
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Kntrl projesini indir
if [ -d "kntrl" ]; then
    echo -e "${YELLOW}kntrl klasörü zaten var, güncelleniyor...${NC}"
    cd kntrl
    git pull
    cd ..
else
    echo -e "${YELLOW}kntrl projesi indiriliyor...${NC}"
    git clone https://github.com/seghobs/kntrl.git
fi

# İsimaly projesini indir
if [ -d "isimaly" ]; then
    echo -e "${YELLOW}isimaly klasörü zaten var, güncelleniyor...${NC}"
    cd isimaly
    git pull
    cd ..
else
    echo -e "${YELLOW}isimaly projesi indiriliyor...${NC}"
    git clone https://github.com/seghobs/isimaly.git
fi

echo -e "\n${YELLOW}[5/7] İzinler ayarlanıyor...${NC}"
chmod -R 777 "$INSTALL_DIR/kntrl"
chmod -R 777 "$INSTALL_DIR/isimaly"

echo -e "\n${YELLOW}[6/7] Flask uygulamaları başlatılıyor...${NC}"

# Her iki projeyi de arka planda başlat
cd "$INSTALL_DIR/kntrl"
if [ -f "flask_app.py" ]; then
    echo -e "${GREEN}kntrl Flask sunucusu başlatılıyor...${NC}"
    nohup python flask_app.py > kntrl.log 2>&1 &
    KNTRL_PID=$!
    echo "kntrl PID: $KNTRL_PID"
else
    echo -e "${RED}HATA: kntrl/flask_app.py bulunamadı!${NC}"
fi

cd "$INSTALL_DIR/isimaly"
if [ -f "flask_app.py" ]; then
    echo -e "${GREEN}isimaly Flask sunucusu başlatılıyor...${NC}"
    nohup python flask_app.py > isimaly.log 2>&1 &
    ISIMALY_PID=$!
    echo "isimaly PID: $ISIMALY_PID"
else
    echo -e "${RED}HATA: isimaly/flask_app.py bulunamadı!${NC}"
fi

# Kısa bir bekleme süresi
sleep 3

echo -e "\n${YELLOW}[7/7] Otomatik başlatma ayarlanıyor...${NC}"

# Boot scripti oluştur
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-flask.sh << 'BOOTEOF'
#!/data/data/com.termux/files/usr/bin/bash

# Wake lock al
termux-wake-lock

# Kısa bekleme
sleep 5

# Projeler dizini
INSTALL_DIR="$HOME/flask_apps"

# Kntrl başlat
if [ -f "$INSTALL_DIR/kntrl/flask_app.py" ]; then
    cd "$INSTALL_DIR/kntrl"
    nohup python flask_app.py > kntrl.log 2>&1 &
fi

# İsimaly başlat
if [ -f "$INSTALL_DIR/isimaly/flask_app.py" ]; then
    cd "$INSTALL_DIR/isimaly"
    nohup python flask_app.py > isimaly.log 2>&1 &
fi
BOOTEOF

chmod +x ~/.termux/boot/start-flask.sh

echo -e "${GREEN}✓ Boot scripti oluşturuldu: ~/.termux/boot/start-flask.sh${NC}"

# Bashrc'ye otomatik başlatma ekle
if ! grep -q "# AutoSev Flask Auto-Start" ~/.bashrc; then
    cat >> ~/.bashrc << 'BASHEOF'

# AutoSev Flask Auto-Start
if [ -f "$HOME/flask_apps/kntrl/flask_app.py" ] || [ -f "$HOME/flask_apps/isimaly/flask_app.py" ]; then
    # Sadece ilk terminalde çalıştır (çift başlatmayı önle)
    if [ -z "$FLASK_STARTED" ]; then
        export FLASK_STARTED=1
        
        # Wake lock al
        termux-wake-lock 2>/dev/null
        
        # Kısa bekleme
        sleep 2
        
        # Kntrl başlat
        if [ -f "$HOME/flask_apps/kntrl/flask_app.py" ]; then
            if ! pgrep -f "flask_app.py" > /dev/null; then
                cd "$HOME/flask_apps/kntrl"
                nohup python flask_app.py > kntrl.log 2>&1 &
                echo "✓ Kntrl Flask sunucusu başlatıldı (PID: $!)"
            fi
        fi
        
        # İsimaly başlat
        if [ -f "$HOME/flask_apps/isimaly/flask_app.py" ]; then
            if ! pgrep -f "isimaly.*flask_app.py" > /dev/null; then
                cd "$HOME/flask_apps/isimaly"
                nohup python flask_app.py > isimaly.log 2>&1 &
                echo "✓ İsimaly Flask sunucusu başlatıldı (PID: $!)"
            fi
        fi
        
        cd ~
        echo "🚀 Flask sunucuları arka planda çalışıyor!"
    fi
fi
# End AutoSev Flask Auto-Start
BASHEOF
    echo -e "${GREEN}✓ Bashrc'ye otomatik başlatma eklendi${NC}"
else
    echo -e "${YELLOW}⚠ Bashrc'de otomatik başlatma zaten mevcut${NC}"
fi

echo -e "\n${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}        Kurulum Tamamlandı! ✓${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "\n${YELLOW}Projeler:${NC}"
echo -e "  📁 Konum: $INSTALL_DIR"
echo -e "  📁 kntrl: $INSTALL_DIR/kntrl"
echo -e "  📁 isimaly: $INSTALL_DIR/isimaly"

echo -e "\n${YELLOW}Log dosyaları:${NC}"
echo -e "  📄 kntrl: $INSTALL_DIR/kntrl/kntrl.log"
echo -e "  📄 isimaly: $INSTALL_DIR/isimaly/isimaly.log"

echo -e "\n${YELLOW}Sunucu durumunu kontrol etmek için:${NC}"
echo -e "  tail -f $INSTALL_DIR/kntrl/kntrl.log"
echo -e "  tail -f $INSTALL_DIR/isimaly/isimaly.log"

echo -e "\n${YELLOW}Sunucuları durdurmak için:${NC}"
echo -e "  pkill -f flask_app.py"

echo -e "\n${YELLOW}Wake lock'u kaldırmak için:${NC}"
echo -e "  termux-wake-unlock"

echo -e "\n${GREEN}✓ Wake lock aktif - Telefon arka planda olsa bile sunucular çalışacak!${NC}"
echo -e "${GREEN}✓ Boot scripti kuruldu - Termux açılınca otomatik başlatacak!${NC}"
echo -e "\n${YELLOW}📢 Önemli: Termux:Boot uygulamasını kurun (isteğe bağlı)${NC}"
echo -e "  Play Store'dan 'Termux:Boot' yüklerseniz telefon açılınca otomatik başlar!"
echo -e "\n${GREEN}Başarılı! Flask sunucuları arka planda çalışıyor.${NC}\n"
