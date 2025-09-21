#!/bin/bash

# quick_https.sh - Super simple HTTPS setup that actually works

echo "🔒 Quick HTTPS Setup for Stock Screener..."

# Stop any existing streamlit
pkill -f streamlit

# Install stunnel for HTTPS proxy
echo "📦 Installing stunnel..."
sudo apt update
sudo apt install stunnel4 openssl -y

# Create SSL certificate
echo "🔐 Creating SSL certificate..."
mkdir -p ~/ssl
openssl req -x509 -newkey rsa:2048 -keyout ~/ssl/key.pem -out ~/ssl/cert.pem -days 365 -nodes -subj "/CN=$(curl -s ifconfig.me)"

# Combine cert and key for stunnel
cat ~/ssl/cert.pem ~/ssl/key.pem > ~/ssl/combined.pem

# Create stunnel config
echo "⚙️ Creating stunnel configuration..."
cat > ~/ssl/stunnel.conf << EOF
[https]
accept = 8443
connect = 127.0.0.1:8501
cert = $HOME/ssl/combined.pem
EOF

# Create startup script
cat > ~/start_https_stockscreener.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting Stock Screener with HTTPS..."

# Start stunnel in background
stunnel ~/ssl/stunnel.conf &
STUNNEL_PID=$!

# Wait a moment for stunnel to start
sleep 2

echo "🔒 HTTPS proxy started on port 8443"
echo "🌐 Starting Streamlit on port 8501..."

# Start Streamlit
cd ~/stockscreener
streamlit run clean_app.py --server.port 8501 --server.address 127.0.0.1 &
STREAMLIT_PID=$!

echo ""
echo "✅ Servers started!"
echo "🌐 Access via: https://$(curl -s ifconfig.me):8443"
echo "⚠️  Browser will show security warning - click 'Advanced' -> 'Proceed'"
echo "🛑 Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap 'echo "🛑 Stopping servers..."; kill $STUNNEL_PID $STREAMLIT_PID; exit' INT
wait
EOF

chmod +x ~/start_https_stockscreener.sh

echo "✅ Quick HTTPS setup complete!"
echo ""
echo "🚀 To start your secure stock screener:"
echo "~/start_https_stockscreener.sh"
echo ""
echo "🌐 Access via: https://$(curl -s ifconfig.me):8443"
echo "⚠️ Browser will show security warning - click 'Advanced' -> 'Proceed'"