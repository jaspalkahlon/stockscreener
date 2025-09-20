#!/bin/bash

# 🚀 Enhanced Stock Screener - One-Click Server Installation
# For Oracle Cloud, Google Cloud, DigitalOcean, or any Ubuntu server

set -e

echo "🚀 Enhanced Stock Screener - Server Installation Starting..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root. Run as ubuntu user."
    exit 1
fi

print_info "Updating system packages..."
sudo apt update && sudo apt upgrade -y
print_status "System updated"

print_info "Installing Python and dependencies..."
sudo apt install -y python3 python3-pip git nginx curl
print_status "Base packages installed"

print_info "Installing Python packages for stock screener..."
pip3 install --user streamlit yfinance ta plotly pandas python-dotenv requests openpyxl scikit-learn numpy scipy textblob vaderSentiment
print_status "Python packages installed"

print_info "Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True)"
print_status "NLTK data downloaded"

print_info "Cloning Enhanced Stock Screener repository..."
cd /home/ubuntu
if [ -d "stockscreener" ]; then
    print_warning "Repository already exists, updating..."
    cd stockscreener
    git pull
else
    git clone https://github.com/jaspalkahlon/stockscreener.git
    cd stockscreener
fi
print_status "Repository ready"

print_info "Setting up environment variables..."
cat > .env << 'EOF'
# Enhanced Stock Screener Environment Variables
NEWSAPI_KEY=deb95d68a1b94efab22bca49f3f7e7ba
HF_API_KEY=
EOF
print_status "Environment configured"

print_info "Creating systemd service for auto-start..."
sudo tee /etc/systemd/system/stockscreener.service > /dev/null << 'EOF'
[Unit]
Description=Enhanced Stock Screener
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/stockscreener
Environment=PATH=/home/ubuntu/.local/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/home/ubuntu/.local/bin/streamlit run enhanced_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
print_status "Service created"

print_info "Configuring Nginx reverse proxy..."
sudo tee /etc/nginx/sites-available/stockscreener > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }
    
    # Handle WebSocket connections
    location /_stcore/stream {
        proxy_pass http://localhost:8501/_stcore/stream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/stockscreener /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
if sudo nginx -t; then
    print_status "Nginx configuration valid"
else
    print_error "Nginx configuration error"
    exit 1
fi

print_info "Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable stockscreener
sudo systemctl start stockscreener
sudo systemctl restart nginx
print_status "Services started"

# Wait a moment for services to start
sleep 5

# Check service status
if sudo systemctl is-active --quiet stockscreener; then
    print_status "Stock Screener service is running"
else
    print_warning "Stock Screener service may not be running properly"
    print_info "Checking logs..."
    sudo journalctl -u stockscreener --no-pager -n 10
fi

if sudo systemctl is-active --quiet nginx; then
    print_status "Nginx service is running"
else
    print_error "Nginx service is not running"
fi

# Get server IP
SERVER_IP=$(curl -s ifconfig.me || curl -s ipinfo.io/ip || echo "Unable to detect IP")

print_info "Setting up firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw allow 8501
print_status "Firewall configured"

echo ""
echo "=================================================="
echo -e "${GREEN}🎉 INSTALLATION COMPLETE! 🎉${NC}"
echo "=================================================="
echo ""
echo -e "${BLUE}📊 Your Enhanced Stock Screener is now live at:${NC}"
echo -e "${YELLOW}🌐 http://$SERVER_IP${NC}"
echo ""
echo -e "${BLUE}📋 Management Commands:${NC}"
echo "• Check status: sudo systemctl status stockscreener"
echo "• View logs: sudo journalctl -u stockscreener -f"
echo "• Restart: sudo systemctl restart stockscreener"
echo "• Update code: cd ~/stockscreener && git pull && sudo systemctl restart stockscreener"
echo ""
echo -e "${BLUE}🔧 Service Details:${NC}"
echo "• Service: stockscreener"
echo "• Port: 8501 (internal), 80 (external)"
echo "• User: ubuntu"
echo "• Auto-start: Enabled"
echo ""
echo -e "${GREEN}✨ Features Available:${NC}"
echo "• 🤖 Machine Learning Predictions"
echo "• 💭 Advanced Sentiment Analysis"
echo "• 📈 Enhanced Technical Analysis"
echo "• 🔬 Advanced Analytics & Risk Metrics"
echo "• 📊 Interactive Charts & Visualizations"
echo ""
echo -e "${YELLOW}⚠️  Important Notes:${NC}"
echo "• Make sure your cloud provider's firewall allows HTTP (port 80)"
echo "• The app will auto-restart if it crashes"
echo "• Updates can be pulled from GitHub anytime"
echo ""
echo -e "${GREEN}🎯 Your professional stock screener is ready for 24/7 use!${NC}"