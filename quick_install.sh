#!/bin/bash
# Termux Panel - Tek Komut Kurulum
# Kullanım: curl -sL https://raw.githubusercontent.com/seghobs/termuxpanel/main/quick_install.sh | bash

echo "🚀 Termux Panel - Hızlı Kurulum"
echo "================================"
echo ""

# Renk kodları
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Python ve Git kontrolü
echo -e "${BLUE}📦 Gerekli paketler kontrol ediliyor...${NC}"

if ! command -v python &> /dev/null; then
    echo -e "${YELLOW}⚙️  Python kuruluyor...${NC}"
    pkg update -y && pkg install python -y
fi

if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}⚙️  Git kuruluyor...${NC}"
    pkg install git -y
fi

echo -e "${GREEN}✓ Python ve Git hazır${NC}"
echo ""

# Eski kurulum varsa temizle
if [ -d "$HOME/termuxpanel" ]; then
    echo -e "${YELLOW}⚠️  Eski kurulum bulundu, temizleniyor...${NC}"
    rm -rf "$HOME/termuxpanel"
fi

# Projeyi indir
echo -e "${BLUE}📥 Proje indiriliyor...${NC}"
cd "$HOME"
git clone https://github.com/seghobs/termuxpanel.git

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Proje indirilemedi!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Proje indirildi${NC}"
echo ""

# Proje dizinine git
cd termuxpanel

# Python paketlerini kur
echo -e "${BLUE}📦 Python paketleri kuruluyor...${NC}"
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Paketler kurulamadı!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Paketler kuruldu${NC}"
echo ""

# Tüm scriptlere chmod ver
echo -e "${BLUE}⚙️  Dosya izinleri ayarlanıyor...${NC}"
chmod -R 755 .
chmod +x *.sh
chmod +x *.py

# Proje klasörünü oluştur ve chmod ver
mkdir -p projects
chmod 777 projects

echo -e "${GREEN}✓ Dosya izinleri ayarlandı${NC}"
echo ""

# install_termux.sh'i çalıştır
echo -e "${BLUE}⚙️  Kurulum scripti çalıştırılıyor...${NC}"
./install_termux.sh

echo ""
echo -e "${GREEN}════════════════════════════════════${NC}"
echo -e "${GREEN}✅ KURULUM TAMAMLANDI!${NC}"
echo -e "${GREEN}════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}🔄 Termux'u yeniden başlatın!${NC}"
echo ""
echo -e "${YELLOW}Termux'u kapatıp tekrar açtığınızda:${NC}"
echo -e "  • Panel otomatik başlayacak"
echo -e "  • Tarayıcı otomatik açılacak"
echo -e "  • ${BLUE}http://127.0.0.1:4747${NC} adresine erişebilirsiniz"
echo ""
echo -e "${YELLOW}Manuel başlatma:${NC}"
echo -e "  cd ~/termuxpanel"
echo -e "  python app.py"
echo ""
