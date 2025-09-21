#!/bin/bash

# setup_autostart.sh - Setup Stock Screener to run automatically

echo "🚀 Setting up Stock Screener Auto-Start..."

# Get current user and paths
USER=$(whoami)
HOME_DIR=$(eval echo ~$USER)
PROJECT_DIR="$HOME_DIR/stockscreener"

echo "👤 User: $USER"
echo "🏠 Home: $HOME_DIR"
echo "📁 Project: $PROJECT_DIR"

# Find streamlit path
STREAMLIT_PATH=$(which streamlit)
if [ -z "$STREAMLIT_PATH" ]; then
    STREAMLIT_PATH="/usr/local/bin/streamlit"
fi

echo "🔍 Streamlit path: $STREAMLIT_PATH"

# Create systemd service file
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/stockscreener.service << EOF
[Unit]
Description=Stock Screener Streamlit Application
Documentation=https://github.com/jaspalkahlon/stockscreener
After=network.target
Wants=network.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=/usr/local/bin:/usr/bin:/bin
ExecStart=$STREAMLIT_PATH run clean_app.py --server.port 8501 --server.address 0.0.0.0
ExecReload=/bin/kill -HUP \$MAINPID
KillMode=mixed
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
echo "🔄 Enabling auto-start service..."
sudo systemctl daemon-reload
sudo systemctl enable stockscreener.service

# Start the service
echo "🚀 Starting Stock Screener service..."
sudo systemctl start stockscreener.service

# Wait a moment for service to start
sleep 3

# Check service status
echo "📊 Service Status:"
sudo systemctl status stockscreener.service --no-pager

# Check if it's running
if sudo systemctl is-active --quiet stockscreener.service; then
    echo ""
    echo "✅ SUCCESS! Stock Screener is now running automatically!"
    echo ""
    echo "🌐 Access your app: http://$(curl -s ifconfig.me):8501"
    echo ""
    echo "🔧 Service Management Commands:"
    echo "   Start:   sudo systemctl start stockscreener"
    echo "   Stop:    sudo systemctl stop stockscreener"
    echo "   Restart: sudo systemctl restart stockscreener"
    echo "   Status:  sudo systemctl status stockscreener"
    echo "   Logs:    sudo journalctl -u stockscreener -f"
    echo ""
    echo "🎉 Your Stock Screener will now:"
    echo "   ✅ Start automatically when server boots"
    echo "   ✅ Restart automatically if it crashes"
    echo "   ✅ Run in background without SSH session"
    echo "   ✅ Keep running 24/7"
else
    echo ""
    echo "❌ Service failed to start. Checking logs..."
    sudo journalctl -u stockscreener.service --no-pager -n 20
    echo ""
    echo "🔧 Troubleshooting:"
    echo "1. Check if streamlit is installed: which streamlit"
    echo "2. Check project directory exists: ls -la $PROJECT_DIR"
    echo "3. Try manual start: cd $PROJECT_DIR && streamlit run clean_app.py"
fi