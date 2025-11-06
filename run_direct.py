#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basit Python Runner - Projeyi doğrudan çalıştırır
"""
import sys
import os
import re

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Kullanım: python run_direct.py <flask_dosyasi.py>")
        sys.exit(1)
    
    flask_file = sys.argv[1]
    project_dir = os.path.dirname(os.path.abspath(flask_file))
    
    # Çalışma dizinini değiştir
    os.chdir(project_dir)
    
    # Proje dizinini sys.path'e ekle
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)
    
    # Üst Flask prosesinden kalan ortam değişkenlerini temizle
    for key in list(os.environ.keys()):
        if key.startswith('WERKZEUG_') or key.startswith('FLASK_'):
            del os.environ[key]
    
    print(f"🚀 Proje: {os.path.basename(flask_file)}")
    print(f"📁 Dizin: {project_dir}")
    
    # Dosyayı oku ve port bul
    with open(flask_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Port bilgisini bul
    port_match = re.search(r'port\s*=\s*(\d+)', code)
    port = int(port_match.group(1)) if port_match else 5000
    
    # Flask(__name__) çağrılarını düzelt - doğru dizinleri kullan
    # Windows path'lerini forward slash'e çevir
    template_path = project_dir.replace('\\', '/')
    static_path = project_dir.replace('\\', '/')
    
    # Flask(__name__) -> Flask(__name__, template_folder='...', static_folder='...')
    replacement = f"app = Flask(__name__, template_folder='{template_path}/templates', static_folder='{static_path}/static')"
    code = re.sub(
        r'app\s*=\s*Flask\s*\(\s*__name__\s*\)',
        replacement,
        code
    )
    
    # debug=True ve use_reloader parametrelerini değiştir
    code = re.sub(
        r'debug\s*=\s*True',
        'debug=False',
        code,
        flags=re.IGNORECASE
    )
    
    code = re.sub(
        r'(app\.run\([^)]*)\)',
        r'\1, use_reloader=False)',
        code
    )
    
    print(f"🌐 Port: {port}")
    print(f"🔗 http://127.0.0.1:{port}")
    print("=" * 60)
    
    # Tarayıcıyı aç
    import webbrowser
    import threading
    def open_browser():
        import time
        time.sleep(2)
        webbrowser.open(f'http://127.0.0.1:{port}')
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Kodu çalıştır
    try:
        exec(compile(code, flask_file, 'exec'), {
            '__name__': '__main__',
            '__file__': flask_file
        })
    except KeyboardInterrupt:
        print("\n⏸️  Durduruldu - Pencere kapanıyor...")
        import time
        time.sleep(1)
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "="*60)
        input("\n⚠️  Hata oluştu! Pencereyi kapatmak için Enter'a basın...")
