#!/usr/bin/env python3
"""
Proje başlatma wrapper scripti
Flask ve Django projelerini Windows'ta sorunsuz çalıştırır
"""
import sys
import os
import re

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Kullanım: python run_project.py <proje_dosyası>")
        sys.exit(1)
    
    project_file = sys.argv[1]
    project_dir = os.path.dirname(os.path.abspath(project_file))
    project_name = os.path.basename(project_file)
    
    # Proje dizinini sys.path'e ekle
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)
    
    # Çalışma dizinini değiştir
    os.chdir(project_dir)
    
    try:
        # Dosya içeriğini oku
        with open(project_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Port ve host bilgilerini bul
        port = 5000
        host = '0.0.0.0'
        
        port_match = re.search(r'port\s*=\s*(\d+)', code)
        if port_match:
            port = int(port_match.group(1))
        
        host_match = re.search(r'host\s*=\s*[\'"]([^\'"]+)[\'"]', code)
        if host_match:
            host = host_match.group(1)
        
        # Son satırdaki app.run() çağrısını kaldır
        # if __name__ == '__main__': bloğunu kaldır
        code_lines = code.split('\n')
        new_code = []
        skip_main_block = False
        
        for line in code_lines:
            if "if __name__ == '__main__'" in line or 'if __name__ == "__main__"' in line:
                skip_main_block = True
                continue
            
            # __main__ bloğundaki girintili satırları atla
            if skip_main_block:
                if line and not line[0].isspace():
                    skip_main_block = False
                else:
                    continue
            
            new_code.append(line)
        
        code = '\n'.join(new_code)
        
        # Kodu çalıştır
        namespace = {'__name__': '__main__', '__file__': project_file}
        exec(code, namespace)
        
        # Flask app nesnesini bul
        app = None
        if 'app' in namespace:
            app = namespace['app']
        
        if app is None:
            print("❌ Flask app nesnesi bulunamadı!")
            sys.exit(1)
        
        # Başlatma mesajı
        print(f"🚀 Proje başlatılıyor: {project_name}")
        print(f"📍 URL: http://127.0.0.1:{port}")
        print(f"⚠️  Debug modu: {'Kapalı (Windows)' if sys.platform == 'win32' else 'Açık'}")
        print(f"\n{'='*50}")
        print("Durdurmak için Ctrl+C basın")
        print('='*50 + '\n')
        
        # Windows'ta debug ve reloader'i kapat
        if sys.platform == 'win32':
            app.run(host=host, port=port, debug=False, use_reloader=False)
        else:
            app.run(host=host, port=port, debug=True)
    
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
