#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows Flask Başlatıcı
Flask projelerini Windows'ta debug modu kapalı olarak başlatır
"""
import sys
import os
import importlib.util

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Kullanım: python start_flask_windows.py <flask_dosyasi.py>")
        sys.exit(1)
    
    flask_file = sys.argv[1]
    project_dir = os.path.dirname(os.path.abspath(flask_file))
    module_name = os.path.basename(flask_file).replace('.py', '')
    
    # Çalışma dizinini değiştir
    os.chdir(project_dir)
    
    # Proje dizinini sys.path'e ekle
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)
    
    # Üst Flask prosesinden kalan ortam değişkenlerini temizle
    for key in list(os.environ.keys()):
        if key.startswith('WERKZEUG_') or key.startswith('FLASK_'):
            del os.environ[key]
    
    print(f"🚀 Proje başlatılıyor: {os.path.basename(flask_file)}")
    print(f"📁 Dizin: {project_dir}")
    print(f"⚙️  Windows modu: Debug ve Reloader kapalı")
    print(f"🌐 Port tespit ediliyor...")
    print("=" * 60)
    
    try:
        # Dosyayı oku ve değiştir
        with open(flask_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        import re
        
        # Port bilgisini bul
        port_match = re.search(r'port\s*=\s*(\d+)', code)
        port = int(port_match.group(1)) if port_match else 5000
        
        # if __name__ == '__main__': bloğunu kaldır ve app.run() parametrelerini değiştir
        # app.run(...) satırlarını bul ve değiştir
        code = re.sub(
            r"if\s+__name__\s*==\s*['\"]__main__['\"]\s*:",
            "if True:",  # Her zaman çalıştır
            code
        )
        
        # app.run() parametrelerini Windows için değiştir
        code = re.sub(
            r'app\.run\s*\([^)]*\)',
            f'app.run(host="0.0.0.0", port={port}, debug=False, use_reloader=False)',
            code
        )
        
        print(f"🌐 Port: {port}")
        print(f"\n✅ Başlatılıyor...")
        print(f"🔗 http://127.0.0.1:{port}")
        print(f"⏸️  Durdurmak için Ctrl+C basın\n")
        print("=" * 60)
        
        # Tarayıcıyı otomatik aç
        import webbrowser
        import threading
        def open_browser():
            import time
            time.sleep(2)  # Flask'in başlamasını bekle
            webbrowser.open(f'http://127.0.0.1:{port}')
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Temiz namespace ile çalıştır - proje kendi modülleriyle çalışmalı
        namespace = {
            '__name__': '__main__',
            '__file__': flask_file,
            '__builtins__': __builtins__,
            '__package__': None,
        }
        
        # sys.argv'ı temizle (wrapper script argümanlarını kaldır)
        original_argv = sys.argv.copy()
        sys.argv = [flask_file]
        
        try:
            exec(code, namespace)
        finally:
            sys.argv = original_argv
    
    except KeyboardInterrupt:
        print("\n\n⏸️  Kullanıcı tarafından durduruldu")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "="*60)
        input("\n⚠️  Pencereyi kapatmak için Enter'a basın...")
        sys.exit(1)
