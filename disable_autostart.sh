#!/bin/bash
# Termux Panel - Otomatik Başlatmayı Devre Dışı Bırak

echo "🔴 Termux Panel otomatik başlatma devre dışı bırakılıyor..."

# .bashrc'den Termux Panel bloğunu sil
sed -i '/# Termux Panel Auto-Start/,/# End Termux Panel/d' ~/.bashrc

echo "✓ Otomatik başlatma kaldırıldı!"
echo ""
echo "Termux'u yeniden başlatın veya:"
echo "  source ~/.bashrc"
echo ""
echo "Panel'i manuel başlatmak için:"
echo "  python app.py"
