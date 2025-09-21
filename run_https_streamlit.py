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

def create_streamlit_config(cert_file, key_file):
    """Create Streamlit configuration for HTTPS"""
    config_dir = Path.home() / ".streamlit"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "config.toml"
    
    config_content = f"""
[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 200

[server.ssl]
certFile = "{cert_file}"
keyFile = "{key_file}"

[browser]
gatherUsageStats = false
"""
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print(f"✅ Streamlit config created: {config_file}")

def run_streamlit_https():
    """Run Streamlit with HTTPS"""
    print("🚀 Starting Stock Screener with HTTPS...")
    
    # Setup SSL certificates
    cert_file, key_file = setup_ssl_certificates()
    if not cert_file or not key_file:
        return
    
    # Create Streamlit config
    create_streamlit_config(cert_file, key_file)
    
    # Run Streamlit
    try:
        print("🌐 Starting Streamlit server...")
        print("📱 Access via: https://your-ip:8501")
        print("⚠️  Browser will show security warning for self-signed certificate")
        print("   Click 'Advanced' -> 'Proceed to site' to continue")
        print("🛑 Press Ctrl+C to stop")
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "clean_app.py"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping Streamlit server...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Streamlit: {e}")
        print("Make sure you're in the stockscreener directory")

if __name__ == "__main__":
    run_streamlit_https()