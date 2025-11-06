#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Termux Panel - Modern Web Yönetim Paneli
Flask + Bootstrap ile geliştirilmiş Termux yönetim arayüzü
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import os
import psutil
import json
import sys
import re
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'termux-panel-secret-key-2024'
app.config['PROJECTS_DIR'] = os.path.join(os.path.dirname(__file__), 'projects')

# Projeler dizinini oluştur
os.makedirs(app.config['PROJECTS_DIR'], exist_ok=True)

def run_command(cmd, shell=True):
    """Komut çalıştır ve sonucu döndür"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
    except Exception as e:
        return {
            'success': False,
            'output': '',
            'error': str(e)
        }

def get_python_version():
    """Python sürümünü al"""
    return sys.version.split()[0]

def get_installed_packages():
    """Kurulu paketleri listele"""
    result = run_command([sys.executable, '-m', 'pip', 'list', '--format=json'], shell=False)
    if result['success']:
        try:
            return json.loads(result['output'])
        except:
            pass
    return []

def get_running_processes():
    """Çalışan Python proseslerini bul"""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
        try:
            pinfo = proc.info
            cmdline = pinfo['cmdline']
            
            if not cmdline:
                continue
                
            # Python proseslerini filtrele
            if 'python' in pinfo['name'].lower():
                cmd_str = ' '.join(cmdline)
                
                # Flask, Django veya Python script kontrolü
                is_flask = 'flask' in cmd_str.lower() or 'app.py' in cmd_str.lower() or 'flask_app.py' in cmd_str.lower()
                is_django = 'django' in cmd_str.lower() or 'manage.py' in cmd_str.lower()
                is_script = cmd_str.endswith('.py')
                
                if is_flask or is_django or is_script:
                    # Port bilgisini bul
                    port = None
                    port_match = re.search(r'(?:--port|:)(\d{4,5})', cmd_str)
                    if port_match:
                        port = int(port_match.group(1))
                    
                    # Proje türünü belirle
                    project_type = 'Python'
                    if is_flask:
                        project_type = 'Flask'
                    elif is_django:
                        project_type = 'Django'
                    
                    # Proje adını bul
                    project_name = 'Unknown'
                    for part in cmdline:
                        if part.endswith('.py'):
                            project_name = os.path.basename(part)
                            break
                    
                    processes.append({
                        'pid': pinfo['pid'],
                        'name': project_name,
                        'type': project_type,
                        'port': port,
                        'cmdline': cmd_str,
                        'started': datetime.fromtimestamp(pinfo['create_time']).strftime('%Y-%m-%d %H:%M:%S')
                    })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return processes

def get_local_projects():
    """Yerel projeleri tara"""
    projects = []
    projects_dir = app.config['PROJECTS_DIR']
    
    if not os.path.exists(projects_dir):
        return projects
    
    for item in os.listdir(projects_dir):
        item_path = os.path.join(projects_dir, item)
        if os.path.isdir(item_path):
            project_info = {
                'name': item,
                'path': item_path,
                'type': 'Unknown',
                'main_file': None,
                'port': None
            }
            
            # Flask projesi kontrolü
            for flask_file in ['app.py', 'flask_app.py', 'main.py', 'run.py']:
                flask_path = os.path.join(item_path, flask_file)
                if os.path.exists(flask_path):
                    project_info['type'] = 'Flask'
                    project_info['main_file'] = flask_file
                    
                    # Port bilgisini dosyadan bul
                    try:
                        with open(flask_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            port_match = re.search(r'port\s*=\s*(\d{4,5})', content)
                            if port_match:
                                project_info['port'] = int(port_match.group(1))
                    except:
                        pass
                    break
            
            # Django projesi kontrolü
            if project_info['type'] == 'Unknown':
                manage_py = os.path.join(item_path, 'manage.py')
                if os.path.exists(manage_py):
                    project_info['type'] = 'Django'
                    project_info['main_file'] = 'manage.py'
                    project_info['port'] = 8000  # Django varsayılan
            
            projects.append(project_info)
    
    return projects

def detect_flask_servers():
    """Çalışan Flask sunucularını tespit et"""
    servers = []
    
    # Proseslerden tespit
    processes = get_running_processes()
    for proc in processes:
        if proc['type'] == 'Flask' and proc['port']:
            servers.append({
                'pid': proc['pid'],
                'port': proc['port'],
                'name': proc['name'],
                'url': f"http://127.0.0.1:{proc['port']}"
            })
    
    return servers

@app.route('/')
def index():
    """Ana sayfa - Dashboard"""
    return render_template('index.html', 
                         python_version=get_python_version())

@app.route('/api/system-info')
def system_info():
    """Sistem bilgilerini döndür"""
    return jsonify({
        'python_version': get_python_version(),
        'platform': sys.platform,
        'total_packages': len(get_installed_packages()),
        'running_processes': len(get_running_processes()),
        'local_projects': len(get_local_projects())
    })

@app.route('/packages')
def packages():
    """Paket yönetimi sayfası"""
    return render_template('packages.html')

@app.route('/api/packages')
def api_packages():
    """Kurulu paketleri listele"""
    packages = get_installed_packages()
    return jsonify({'success': True, 'packages': packages})

@app.route('/api/packages/install', methods=['POST'])
def install_package():
    """Paket kur"""
    package_name = request.json.get('package')
    if not package_name:
        return jsonify({'success': False, 'error': 'Paket adı gerekli'})
    
    result = run_command([sys.executable, '-m', 'pip', 'install', package_name], shell=False)
    return jsonify(result)

@app.route('/api/packages/uninstall', methods=['POST'])
def uninstall_package():
    """Paket kaldır"""
    package_name = request.json.get('package')
    if not package_name:
        return jsonify({'success': False, 'error': 'Paket adı gerekli'})
    
    result = run_command([sys.executable, '-m', 'pip', 'uninstall', '-y', package_name], shell=False)
    return jsonify(result)

@app.route('/projects')
def projects():
    """Projeler sayfası"""
    return render_template('projects.html')

@app.route('/api/projects')
def api_projects():
    """Projeleri listele"""
    projects = get_local_projects()
    return jsonify({'success': True, 'projects': projects})

@app.route('/api/projects/clone', methods=['POST'])
def clone_project():
    """GitHub projesini klonla"""
    repo_url = request.json.get('repo_url')
    if not repo_url:
        return jsonify({'success': False, 'error': 'Repo URL gerekli'})
    
    # Proje adını URL'den çıkar
    project_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
    project_path = os.path.join(app.config['PROJECTS_DIR'], project_name)
    
    # Klonla
    result = run_command(f'git clone {repo_url} "{project_path}"')
    
    if result['success']:
        # Linux/Termux için chmod
        if sys.platform != 'win32':
            os.chmod(project_path, 0o777)
            for root, dirs, files in os.walk(project_path):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o777)
                for f in files:
                    os.chmod(os.path.join(root, f), 0o777)
        
        return jsonify({
            'success': True,
            'message': f'Proje başarıyla indirildi: {project_name}',
            'project_name': project_name
        })
    
    return jsonify(result)

@app.route('/api/projects/start', methods=['POST'])
def start_project():
    """Proje başlat"""
    project_name = request.json.get('project')
    if not project_name:
        return jsonify({'success': False, 'error': 'Proje adı gerekli'})
    
    project_path = os.path.join(app.config['PROJECTS_DIR'], project_name)
    
    # Ana dosyayı bul
    main_file = None
    for flask_file in ['flask_app.py', 'app.py', 'main.py', 'run.py']:
        file_path = os.path.join(project_path, flask_file)
        if os.path.exists(file_path):
            main_file = flask_file
            break
    
    if not main_file:
        # Django kontrolü
        manage_py = os.path.join(project_path, 'manage.py')
        if os.path.exists(manage_py):
            # Django projesini başlat
            try:
                if sys.platform == 'win32':
                    # Windows için arka planda çalıştır (terminal açık kalacak)
                    cmd = f'start "Django: {project_name}" cmd /k "cd /d "{project_path}" && {sys.executable} manage.py runserver"'
                    subprocess.Popen(
                        cmd,
                        shell=True,
                        cwd=project_path
                    )
                else:
                    # Linux/Termux için
                    log_file = os.path.join(project_path, f'{project_name}.log')
                    with open(log_file, 'w') as f:
                        subprocess.Popen(
                            [sys.executable, 'manage.py', 'runserver'],
                            cwd=project_path,
                            stdout=f,
                            stderr=f,
                            start_new_session=True
                        )
                return jsonify({'success': True, 'message': 'Django projesi arka planda başlatıldı'})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        return jsonify({'success': False, 'error': 'Ana dosya bulunamadı'})
    
    # Flask projesini başlat
    try:
        main_file_path = os.path.join(project_path, main_file)
        
        if sys.platform == 'win32':
            # Windows için: basit runner kullan
            wrapper_script = os.path.join(os.path.dirname(__file__), 'run_direct.py')
            
            # BAT dosyası içeriği
            bat_content = f'''@echo off
title {project_name}
cd /d "{project_path}"
"{sys.executable}" "{wrapper_script}" "{main_file_path}"
'''
            
            # Geçici BAT dosyasını proje dizinine yaz
            bat_file_path = os.path.join(project_path, f'_start_{project_name}.bat')
            with open(bat_file_path, 'w', encoding='utf-8') as f:
                f.write(bat_content)
            
            # BAT dosyasını yeni pencerede başlat
            subprocess.Popen(
                ['cmd', '/c', 'start', bat_file_path],
                cwd=project_path
            )
        else:
            # Linux/Termux için arka planda çalıştır
            # Log dosyasına yazdır
            log_file = os.path.join(project_path, f'{project_name}.log')
            with open(log_file, 'w') as f:
                subprocess.Popen(
                    [sys.executable, main_file_path],
                    cwd=project_path,
                    stdout=f,
                    stderr=f,
                    start_new_session=True
                )
        
        return jsonify({'success': True, 'message': 'Proje arka planda başlatıldı'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/projects/delete', methods=['POST'])
def delete_project():
    """Projeyi sil"""
    project_name = request.json.get('project')
    if not project_name:
        return jsonify({'success': False, 'error': 'Proje adı gerekli'})
    
    project_path = os.path.join(app.config['PROJECTS_DIR'], project_name)
    
    try:
        import shutil
        import stat
        
        # Windows'ta read-only dosyaları silmek için özel fonksiyon
        def remove_readonly(func, path, excinfo):
            """Read-only dosyaları silebilmek için izinleri değiştir"""
            os.chmod(path, stat.S_IWRITE)
            func(path)
        
        # Projeyi sil (read-only dosyalar için onerror callback kullan)
        shutil.rmtree(project_path, onerror=remove_readonly)
        return jsonify({'success': True, 'message': 'Proje silindi'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/processes')
def processes():
    """Prosesler sayfası"""
    return render_template('processes.html')

@app.route('/api/processes')
def api_processes():
    """Çalışan prosesleri listele"""
    processes = get_running_processes()
    return jsonify({'success': True, 'processes': processes})

@app.route('/api/processes/kill', methods=['POST'])
def kill_process():
    """Prosesi durdur"""
    pid = request.json.get('pid')
    if not pid:
        return jsonify({'success': False, 'error': 'PID gerekli'})
    
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=3)
        return jsonify({'success': True, 'message': 'Proses durduruldu'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/servers')
def servers():
    """Flask sunucuları sayfası"""
    return render_template('servers.html')

@app.route('/api/servers')
def api_servers():
    """Çalışan sunucuları listele"""
    servers = detect_flask_servers()
    return jsonify({'success': True, 'servers': servers})

if __name__ == '__main__':
    # Termux için 0.0.0.0 kullan
    app.run(host='0.0.0.0', port=5000, debug=True)
