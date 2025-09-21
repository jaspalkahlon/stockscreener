#!/bin/bash

# setup_self_signed_https.sh - Quick HTTPS setup with self-signed certificate

echo "🔒 Setting up Self-Signed HTTPS for Stock Screener..."

# Create SSL directory
mkdir -p ~/ssl

# Generate self-signed certificate
echo "🔐 Generating self-signed SSL certificate..."
openssl req -x509 -newkey rsa:4096 -keyout ~/ssl/key.pem -out ~/ssl/cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

echo "✅ SSL certificate generated!"

# Create HTTPS Streamlit config
echo "⚙️ Creating Streamlit HTTPS configuration..."
mkdir -p ~/.streamlit

cat > ~/.streamlit/config.toml << 'EOF'
[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false

[server.ssl]
certFile = "~/ssl/cert.pem"
keyFile = "~/ssl/key.pem"
EOF

echo "✅ HTTPS setup complete!"
echo ""
echo "🚀 To run with HTTPS:"
echo "streamlit run clean_app.py"
echo ""
echo "🌐 Access via: https://your-ip:8501"
echo "⚠️ Note: Browser will show security warning for self-signed certificate"
echo "Click 'Advanced' -> 'Proceed to site' to continue"