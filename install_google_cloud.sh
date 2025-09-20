#!/bin/bash

# 🌐 Enhanced Stock Screener - Google Cloud Installation
# Optimized for Google Cloud Platform Ubuntu instances

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_header() {
    echo -e "${PURPLE}🚀 $1${NC}"
}

# Header
clear
print_header "Enhanced Stock Screener - Google Cloud Installation"
echo "============================================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root. Run as your regular user."
    exit 1
fi

# Detect if running on Google Cloud
if curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/name &>/dev/null; then
    print_info "✅ Google Cloud Platform detected"
    INSTANCE_NAME=$(curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/name)
    ZONE=$(curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/zone | cut -d/ -f4)
    EXTERNAL_IP=$(curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip)
    print_info "Instance: $INSTANCE_NAME in zone $ZONE"
    print_info "External IP: $EXTERNAL_IP"
else
    print_warning "Not running on Google Cloud, but continuing with installation..."
fi

echo ""

# Update system
print_info "Updating system packages..."
sudo apt update && sudo apt upgrade -y
print_status "System updated successfully"

# Install essential packages
print_info "Installing essential packages..."
sudo apt install -y python3 python3-pip git nginx curl htop unzip software-properties-common
print_status "Essential packages installed"

# Install Python packages
print_info "Installing Python packages for Enhanced Stock Screener..."
pip3 install --user --upgrade pip
pip3 install --user streamlit yfinance ta plotly pandas python-dotenv requests openpyxl scikit-learn numpy scipy textblob vaderSentiment

# Add local bin to PATH if not already there
if ! echo $PATH | grep -q "$HOME/.local/bin"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/.local/bin:$PATH"
fi

print_status "Python packages installed successfully"

# Download NLTK data
print_info "Downloading NLTK data..."
python3 -c "
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('punkt', quiet=True)
nltk.download('brown', quiet=True)
print('NLTK data downloaded successfully')
"
print_status "NLTK data downloaded"

# Clone repository
print_info "Cloning Enhanced Stock Screener repository..."
cd $HOME
if [ -d "stockscreener" ]; then
    print_warning "Repository already exists, updating..."
    cd stockscreener
    git pull
else
    git clone https://github.com/jaspalkahlon/stockscreener.git
    cd stockscreener
fi
print_status "Repository ready"

# Set up environment
print_info "Setting up environment variables..."
cat > .env << 'EOF'
# Enhanced Stock Screener Environment Variables
NEWSAPI_KEY=deb95d68a1b94efab22bca49f3f7e7ba
HF_API_KEY=
EOF
print_status "Environment configured"

# Create systemd service
print_info "Creating systemd service for auto-start..."
sudo tee /etc/systemd/system/stockscreener.service > /dev/null << EOF
[Unit]
Description=Enhanced Stock Screener
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/stockscreener
Environment=PATH=$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=$HOME/.local/bin/streamlit run enhanced_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true --server.enableCORS false --server.enableXsrfProtection false
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
print_status "Systemd service created"

# Configure Nginx
print_info "Configuring Nginx reverse proxy..."
sudo tee /etc/nginx/sites-available/stockscreener > /dev/null << 'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    
    client_max_body_size 100M;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    
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
        proxy_connect_timeout 60;
        proxy_send_timeout 60;
    }
    
    # Handle WebSocket connections for Streamlit
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
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Enable Nginx site
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/stockscreener /etc/nginx/sites-enabled/

# Test Nginx configuration
if sudo nginx -t; then
    print_status "Nginx configuration is valid"
else
    print_error "Nginx configuration error"
    exit 1
fi

# Configure firewall (Google Cloud specific)
print_info "Configuring firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw allow 8501/tcp
print_status "Firewall configured"

# Start services
print_info "Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable stockscreener
sudo systemctl start stockscreener
sudo systemctl restart nginx
print_status "Services started"

# Wait for services to start
print_info "Waiting for services to initialize..."
sleep 10

# Check service status
print_info "Checking service status..."
if sudo systemctl is-active --quiet stockscreener; then
    print_status "Stock Screener service is running"
else
    print_warning "Stock Screener service may not be running properly"
    print_info "Checking logs..."
    sudo journalctl -u stockscreener --no-pager -n 5
fi

if sudo systemctl is-active --quiet nginx; then
    print_status "Nginx service is running"
else
    print_error "Nginx service is not running"
    sudo systemctl status nginx --no-pager -n 5
fi

# Test local connection
print_info "Testing local connection..."
if curl -s --connect-timeout 10 http://localhost:8501/_stcore/health > /dev/null; then
    print_status "Local Streamlit connection successful"
elif curl -s --connect-timeout 10 http://localhost:8501 > /dev/null; then
    print_status "Local Streamlit connection successful (alternative check)"
else
    print_warning "Local connection test failed, but service may still be starting"
fi

# Get external IP
if [ -n "$EXTERNAL_IP" ]; then
    SERVER_IP=$EXTERNAL_IP
else
    SERVER_IP=$(curl -s --connect-timeout 5 ifconfig.me 2>/dev/null || curl -s --connect-timeout 5 ipinfo.io/ip 2>/dev/null || echo "Unable to detect")
fi

# Create management scripts
print_info "Creating management scripts..."

# Status check script
cat > $HOME/check_status.sh << 'EOF'
#!/bin/bash
echo "🔍 Enhanced Stock Screener Status"
echo "================================"
echo "Service Status:"
sudo systemctl status stockscreener --no-pager -l
echo ""
echo "Nginx Status:"
sudo systemctl status nginx --no-pager -l
echo ""
echo "Recent Logs:"
sudo journalctl -u stockscreener --no-pager -n 10
EOF
chmod +x $HOME/check_status.sh

# Update script
cat > $HOME/update_screener.sh << 'EOF'
#!/bin/bash
echo "🔄 Updating Enhanced Stock Screener..."
cd $HOME/stockscreener
git pull
sudo systemctl restart stockscreener
echo "✅ Update complete!"
EOF
chmod +x $HOME/update_screener.sh

print_status "Management scripts created"

# Final output
echo ""
echo "============================================================"
print_header "🎉 INSTALLATION COMPLETE! 🎉"
echo "============================================================"
echo ""
print_info "📊 Your Enhanced Stock Screener is now live!"
echo ""
if [ -n "$EXTERNAL_IP" ]; then
    echo -e "${YELLOW}🌐 Access your stock screener at:${NC}"
    echo -e "${GREEN}   http://$EXTERNAL_IP${NC}"
    echo ""
    echo -e "${BLUE}📱 Mobile friendly URL:${NC}"
    echo -e "${GREEN}   http://$EXTERNAL_IP${NC}"
else
    echo -e "${YELLOW}🌐 Access your stock screener at:${NC}"
    echo -e "${GREEN}   http://$SERVER_IP${NC}"
    echo ""
    echo -e "${BLUE}💡 Find your external IP in Google Cloud Console:${NC}"
    echo "   Compute Engine → VM instances → External IP"
fi

echo ""
echo -e "${BLUE}🔧 Management Commands:${NC}"
echo "• Check status: ./check_status.sh"
echo "• Update app: ./update_screener.sh"
echo "• View logs: sudo journalctl -u stockscreener -f"
echo "• Restart: sudo systemctl restart stockscreener"
echo ""
echo -e "${BLUE}📋 Service Details:${NC}"
echo "• Service: stockscreener"
echo "• Port: 8501 (internal), 80 (external)"
echo "• Auto-start: ✅ Enabled"
echo "• SSL: Ready for setup (optional)"
echo ""
echo -e "${GREEN}✨ Features Available:${NC}"
echo "• 🤖 Machine Learning Predictions"
echo "• 💭 Advanced Sentiment Analysis (NewsAPI configured)"
echo "• 📈 Enhanced Technical Analysis"
echo "• 🔬 Advanced Analytics & Risk Metrics"
echo "• 📊 Interactive Charts & Visualizations"
echo "• 📱 Mobile Responsive Design"
echo ""
echo -e "${YELLOW}⚠️  Important Notes:${NC}"
echo "• Make sure Google Cloud firewall allows HTTP traffic"
echo "• The app will auto-restart if it crashes"
echo "• Updates can be pulled from GitHub anytime"
echo "• Monitor your Google Cloud billing dashboard"
echo ""
echo -e "${PURPLE}🎯 Your professional stock screener is ready for 24/7 use!${NC}"
echo ""

# Final connectivity test
if [ -n "$EXTERNAL_IP" ]; then
    print_info "Testing external connectivity..."
    if curl -s --connect-timeout 15 "http://$EXTERNAL_IP/health" > /dev/null 2>&1; then
        print_status "✅ External access confirmed!"
    else
        print_warning "External access test inconclusive (may need a few more minutes to start)"
        echo "   Try accessing http://$EXTERNAL_IP in 2-3 minutes"
    fi
fi

echo ""
print_header "🚀 Setup Complete - Enjoy your Enhanced Stock Screener! 🚀"