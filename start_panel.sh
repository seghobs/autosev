#!/bin/bash
# Termux Panel - Manuel Başlatma

echo "🚀 Termux Panel Başlatılıyor..."

# Panel zaten çalışıyor mu?
if pgrep -f "python.*app.py" > /dev/null; then
    EXISTING_PID=$(pgrep -f "python.*app.py")
    echo "⚠️  Panel zaten çalışıyor (PID: $EXISTING_PID)"
    echo "🔗 URL: http://127.0.0.1:5000"
    echo ""
    echo "Durdurmak için: pkill -f 'python.*app.py'"
    exit 0
fi

# Proje dizinini bul
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Arka planda başlat - daemon olarak
setsid python app.py > ~/termux-panel.log 2>&1 < /dev/null &
PANEL_PID=$!

# Process'i tamamen bağımsız yap
disown

echo "✓ Panel başlatıldı (PID: $PANEL_PID)"
echo "🔗 URL: http://127.0.0.1:5000"
echo "⚡ Termux kapansa bile çalışmaya devam edecek!"
echo ""

# Tarayıcıyı aç
sleep 2
termux-open-url http://127.0.0.1:5000 2>/dev/null

echo "Durdurmak için: pkill -f 'python.*app.py'"
echo "Logları görmek için: tail -f ~/termux-panel.log"
echo "Durum kontrolü: pgrep -f 'python.*app.py'"
