#!/bin/bash

# setup_cloudflare_tunnel.sh - Setup secure HTTPS using Cloudflare Tunnel

echo "☁️ Setting up Cloudflare Tunnel for Stock Screener..."

# Download cloudflared
echo "📥 Downloading Cloudflare Tunnel..."
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Authenticate with Cloudflare
echo "🔐 Please authenticate with Cloudflare..."
echo "This will open a browser window for authentication"
cloudflared tunnel login

# Create tunnel
echo "🚇 Creating tunnel..."
TUNNEL_NAME="stockscreener-$(date +%s)"
cloudflared tunnel create $TUNNEL_NAME

# Get tunnel ID
TUNNEL_ID=$(cloudflared tunnel list | grep $TUNNEL_NAME | awk '{print $1}')

# Create config file
echo "⚙️ Creating tunnel configuration..."
mkdir -p ~/.cloudflared

cat > ~/.cloudflared/config.yml << EOF
tunnel: $TUNNEL_ID
credentials-file: ~/.cloudflared/$TUNNEL_ID.json

ingress:
  - hostname: your-domain.com  # Replace with your domain
    service: http://localhost:8501
  - service: http_status:404
EOF

echo "✅ Cloudflare Tunnel setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit ~/.cloudflared/config.yml and replace 'your-domain.com' with your actual domain"
echo "2. Add DNS record: cloudflared tunnel route dns $TUNNEL_NAME your-domain.com"
echo "3. Start tunnel: cloudflared tunnel run $TUNNEL_NAME"
echo "4. Start Streamlit: streamlit run clean_app.py --server.port 8501"
echo ""
echo "🌐 Your app will be available at: https://your-domain.com"
echo "🔒 Automatically secured with Cloudflare SSL"