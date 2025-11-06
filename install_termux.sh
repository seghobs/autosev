#!/bin/bash
# Termux Panel - Otomatik Kurulum Scripti

echo "🚀 Termux Panel Kurulumu Başlatılıyor..."
echo ""

# Renk kodları
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Python kontrolü
echo -e "${BLUE}Python kontrolü yapılıyor...${NC}"
if ! command -v python &> /dev/null; then
    echo -e "${RED}Python bulunamadı! Kuruluyor...${NC}"
    pkg install python -y
else
    echo -e "${GREEN}✓ Python kurulu${NC}"
fi

# Git kontrolü
echo -e "${BLUE}Git kontrolü yapılıyor...${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${RED}Git bulunamadı! Kuruluyor...${NC}"
    pkg install git -y
else
    echo -e "${GREEN}✓ Git kurulu${NC}"
fi

# Python paketlerini kur
echo ""
echo -e "${BLUE}Python paketleri kuruluyor...${NC}"
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Paketler başarıyla kuruldu${NC}"
else
    echo -e "${RED}✗ Paket kurulumunda hata oluştu${NC}"
    exit 1
fi

# Tüm dosya ve klasörlere izin ver
echo -e "${BLUE}Dosya izinleri ayarlanıyor...${NC}"

# Tüm scriptlere çalıştırma izni
chmod +x *.sh 2>/dev/null
chmod +x *.py 2>/dev/null

# Projects klasörü
mkdir -p projects
chmod 777 projects

# Static ve templates
chmod -R 755 static 2>/dev/null
chmod -R 755 templates 2>/dev/null

echo -e "${GREEN}✓ Dosya izinleri ayarlandı${NC}"

# Otomatik başlatma yapılandırması
echo ""
echo -e "${BLUE}Otomatik başlatma ayarlanıyor...${NC}"

# Proje dizinini al
PROJECT_DIR="$(pwd)"

# .bashrc dosyasını kontrol et ve oluştur
if [ ! -f ~/.bashrc ]; then
    touch ~/.bashrc
fi

# Eski Termux Panel girişlerini temizle
sed -i '/# Termux Panel Auto-Start/,/# End Termux Panel/d' ~/.bashrc

# Yeni otomatik başlatma scripti ekle
cat >> ~/.bashrc << 'AUTOSTART'

# Termux Panel Auto-Start
if [ -z "$TERMUX_PANEL_STARTED" ]; then
    export TERMUX_PANEL_STARTED=1
    
    echo ""
    echo "\033[0;36m════════════════════════════════════\033[0m"
    echo "\033[0;32m🚀 Termux Panel Başlatılıyor...\033[0m"
    echo "\033[0;36m════════════════════════════════════\033[0m"
    echo ""
    
    # Proje dizinine git
AUTOSTART

echo "    cd \"$PROJECT_DIR\"" >> ~/.bashrc

cat >> ~/.bashrc << 'AUTOSTART'
    
    # Arka planda başlat (Termux kapanınca panel de kapanacak)
    python app.py > ~/termux-panel.log 2>&1 &
    PANEL_PID=$!
    
    echo "\033[0;32m✓ Panel başlatıldı (PID: $PANEL_PID)\033[0m"
    echo "\033[0;34m🔗 URL: http://127.0.0.1:4747\033[0m"
    echo ""
    
    # 2 saniye bekle ve tarayıcıyı aç
    sleep 2
    termux-open-url http://127.0.0.1:4747 2>/dev/null
    
    echo "\033[0;33mDurdurmak için: kill $PANEL_PID\033[0m"
    echo "\033[0;33mLogları görmek için: tail -f ~/termux-panel.log\033[0m"
    echo ""
fi
# End Termux Panel
AUTOSTART

echo -e "${GREEN}✓ Otomatik başlatma ayarlandı${NC}"
echo -e "${BLUE}  Termux her açıldığında panel otomatik başlayacak!${NC}"

echo ""
echo -e "${GREEN}════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Kurulum tamamlandı!${NC}"
echo -e "${GREEN}════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Manuel başlatmak için:${NC}"
echo "  python app.py"
echo ""
echo -e "${BLUE}Otomatik başlatmayı devre dışı bırakmak için:${NC}"
echo "  sed -i '/# Termux Panel Auto-Start/,/# End Termux Panel/d' ~/.bashrc"
echo ""
echo -e "${BLUE}🔄 Termux'u yeniden başlatın veya:${NC}"
echo "  source ~/.bashrc"
echo ""
