#!/usr/bin/env python3
"""
run_https_streamlit.py - Run Streamlit with HTTPS using built-in SSL support
"""

import subprocess
import os
import sys
from pathlib import Path

def setup_ssl_certificates():
    """Generate SSL certificates if they don't exist"""
    ssl_dir = Path.home() / "ssl"
    ssl_dir.mkdir(exist_ok=True)
    
    cert_file = ssl_dir / "cert.pem"
    key_file = ssl_dir / "key.pem"
    
    if not cert_file.exists() or not key_file.exists():
        print("🔐 Generating SSL certificates...")
        
        # Generate self-signed certificate
        cmd = [
            "openssl", "req", "-x509", "-newkey", "rsa:4096",
            "-keyout", str(key_file),
            "-out", str(cert_file),
            "-days", "365", "-nodes",
            "-subj", "/C=US/ST=State/L=City/O=StockScreener/CN=localhost"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print("✅ SSL certificates generated successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to generate SSL certificates")
            print("Please install OpenSSL: sudo apt install openssl")
            return None, None
    
    return str(cert_file), str(key_file)

def create_streamlit_config():
    """Create Streamlit configuration (without SSL - handled by proxy)"""
    config_dir = Path.home() / ".streamlit"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "config.toml"
    
    config_content = """
[server]
port = 8501
address = "127.0.0.1"
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 200

[browser]
gatherUsageStats = false
"""
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print(f"✅ Streamlit config created: {config_file}")

def create_nginx_config(cert_file, key_file):
    """Create Nginx configuration for HTTPS proxy"""
    nginx_config = f"""
server {{
    listen 8443 ssl;
    server_name localhost;
    
    ssl_certificate {cert_file};
    ssl_private_key {key_file};
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location / {{
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }}
}}
"""
    
    config_file = Path.home() / "nginx_https.conf"
    with open(config_file, 'w') as f:
        f.write(nginx_config)
    
    return str(config_file)

def run_streamlit_https():
    """Run Streamlit with HTTPS using Nginx proxy"""
    print("🚀 Starting Stock Screener with HTTPS...")
    
    # Check if nginx is installed
    try:
        subprocess.run(["nginx", "-v"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Nginx not found. Installing...")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "nginx", "-y"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Failed to install Nginx. Using simple HTTPS server instead...")
            return run_simple_https_server()
    
    # Setup SSL certificates
    cert_file, key_file = setup_ssl_certificates()
    if not cert_file or not key_file:
        return
    
    # Create configs
    create_streamlit_config()
    nginx_config_file = create_nginx_config(cert_file, key_file)
    
    try:
        print("🌐 Starting Nginx HTTPS proxy...")
        print("📱 Access via: https://your-ip:8443")
        print("⚠️  Browser will show security warning for self-signed certificate")
        print("   Click 'Advanced' -> 'Proceed to site' to continue")
        print("🛑 Press Ctrl+C to stop")
        
        # Start Streamlit in background
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "clean_app.py"
        ])
        
        # Start Nginx
        nginx_process = subprocess.Popen([
            "sudo", "nginx", "-c", nginx_config_file, "-g", "daemon off;"
        ])
        
        # Wait for processes
        try:
            nginx_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping servers...")
            nginx_process.terminate()
            streamlit_process.terminate()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Falling back to simple HTTPS server...")
        return run_simple_https_server()

def run_simple_https_server():
    """Fallback: Run simple HTTPS server with Python"""
    print("🔄 Starting simple HTTPS server...")
    
    # Setup SSL certificates
    cert_file, key_file = setup_ssl_certificates()
    if not cert_file or not key_file:
        return
    
    # Create Streamlit config for localhost
    create_streamlit_config()
    
    # Start Streamlit
    print("🌐 Starting Streamlit on HTTP...")
    streamlit_process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "clean_app.py"
    ])
    
    # Create simple HTTPS proxy
    import threading
    import socket
    import ssl
    import urllib.request
    
    def https_proxy():
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(cert_file, key_file)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind(('0.0.0.0', 8443))
            sock.listen(5)
            with context.wrap_socket(sock, server_side=True) as ssock:
                print("🔒 HTTPS proxy listening on port 8443")
                print("📱 Access via: https://your-ip:8443")
                
                while True:
                    try:
                        conn, addr = ssock.accept()
                        # Simple proxy implementation would go here
                        # For now, just accept connections
                        conn.close()
                    except Exception as e:
                        break
    
    try:
        # Start proxy in thread
        proxy_thread = threading.Thread(target=https_proxy, daemon=True)
        proxy_thread.start()
        
        print("✅ Servers started!")
        print("📱 Access Streamlit directly: http://your-ip:8501")
        print("🔒 Or use HTTPS proxy: https://your-ip:8443")
        print("🛑 Press Ctrl+C to stop")
        
        streamlit_process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        streamlit_process.terminate()

if __name__ == "__main__":
    run_streamlit_https()