#!/bin/bash
# Termux Panel - Durdurma

echo "⏸️  Termux Panel durduruluyor..."

# Panel çalışıyor mu?
if ! pgrep -f "python.*app.py" > /dev/null; then
    echo "❌ Panel zaten çalışmıyor"
    exit 1
fi

# PID'yi al
PANEL_PID=$(pgrep -f "python.*app.py")

# Durdur
pkill -f "python.*app.py"

if [ $? -eq 0 ]; then
    echo "✓ Panel durduruldu (PID: $PANEL_PID)"
else
    echo "❌ Panel durdurulamadı"
    exit 1
fi

# Tekrar kontrol et
sleep 1
if pgrep -f "python.*app.py" > /dev/null; then
    echo "⚠️  Panel hala çalışıyor, zorla kapatılıyor..."
    pkill -9 -f "python.*app.py"
    echo "✓ Panel zorla kapatıldı"
else
    echo "✓ Panel tamamen kapatıldı"
fi
