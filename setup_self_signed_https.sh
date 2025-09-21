#!/bin/bash

# setup_self_signed_https.sh - Quick HTTPS setup with Nginx reverse proxy

echo "🔒 Setting up HTTPS for Stock Screener with Nginx..."

# Update system
sudo apt update

# Install Nginx and OpenSSL
echo "📦 Installing Nginx and OpenSSL..."
sudo apt install nginx openssl -y

# Create SSL directory
mkdir -p ~/ssl

# Generate self-signed certificate
echo "🔐 Generating self-signed SSL certificate..."
openssl req -x509 -newkey rsa:4096 -keyout ~/ssl/key.pem -out ~/ssl/cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=StockScreener/CN=$(curl -s ifconfig.me)"

echo "✅ SSL certificate generated!"

# Create Nginx configuration
echo "⚙️ Creating Nginx HTTPS configuration..."
sudo tee /etc/nginx/sites-available/stockscreener-https << EOF
server {
    listen 443 ssl;
    server_name _;
    
    ssl_certificate $HOME/ssl/cert.pem;
    ssl_private_key $HOME/ssl/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        
        # WebSocket support
        proxy_set_header X-Forwarded-Host \$server_name;
        proxy_set_header X-Forwarded-Server \$host;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name _;
    return 301 https://\$server_name\$request_uri;
}
EOF

# Enable the site
echo "✅ Enabling Nginx HTTPS site..."
sudo ln -sf /etc/nginx/sites-available/stockscreener-https /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
sudo nginx -t

# Start and enable Nginx
echo "🚀 Starting Nginx..."
sudo systemctl restart nginx
sudo systemctl enable nginx

# Create Streamlit config (HTTP only, Nginx handles HTTPS)
echo "⚙️ Creating Streamlit configuration..."
mkdir -p ~/.streamlit

cat > ~/.streamlit/config.toml << 'EOF'
[server]
port = 8501
address = "127.0.0.1"
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 200

[browser]
gatherUsageStats = false
EOF

# Create startup script
cat > ~/start_secure_stockscreener.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Secure Stock Screener..."
echo "🌐 Access via: https://$(curl -s ifconfig.me)"
echo "⚠️  Browser will show security warning for self-signed certificate"
echo "   Click 'Advanced' -> 'Proceed to site' to continue"
echo "🛑 Press Ctrl+C to stop"
echo ""

cd ~/stockscreener
streamlit run clean_app.py
EOF

chmod +x ~/start_secure_stockscreener.sh

echo "✅ HTTPS setup complete!"
echo ""
echo "🚀 To start your secure stock screener:"
echo "~/start_secure_stockscreener.sh"
echo ""
echo "🌐 Access via: https://$(curl -s ifconfig.me)"
echo "⚠️ Browser will show security warning - click 'Advanced' -> 'Proceed'"
echo ""
echo "🔧 Manual start:"
echo "streamlit run clean_app.py"
echo "# Then access via HTTPS URL above"