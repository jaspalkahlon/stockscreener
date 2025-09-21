#!/bin/bash

# manage_stockscreener.sh - Easy management script for Stock Screener service

show_help() {
    echo "🚀 Stock Screener Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     - Start the Stock Screener service"
    echo "  stop      - Stop the Stock Screener service"
    echo "  restart   - Restart the Stock Screener service"
    echo "  status    - Show service status"
    echo "  logs      - Show live logs"
    echo "  enable    - Enable auto-start on boot"
    echo "  disable   - Disable auto-start on boot"
    echo "  install   - Install/setup the service"
    echo "  uninstall - Remove the service"
    echo "  url       - Show access URL"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs"
    echo "  $0 status"
}

get_server_ip() {
    # Try multiple methods to get external IP
    IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || curl -s icanhazip.com 2>/dev/null)
    if [ -z "$IP" ]; then
        IP=$(hostname -I | awk '{print $1}')
    fi
    echo "$IP"
}

show_url() {
    IP=$(get_server_ip)
    echo "🌐 Access your Stock Screener:"
    echo "   http://$IP:8501"
    echo ""
    echo "📱 Features available:"
    echo "   ✅ Technical Analysis Charts"
    echo "   ✅ AI Price Predictions"
    echo "   ✅ Sentiment Analysis"
    echo "   ✅ Risk Metrics"
    echo "   ✅ Mobile Responsive"
}

case "$1" in
    start)
        echo "🚀 Starting Stock Screener..."
        sudo systemctl start stockscreener.service
        sleep 2
        if sudo systemctl is-active --quiet stockscreener.service; then
            echo "✅ Stock Screener started successfully!"
            show_url
        else
            echo "❌ Failed to start. Check logs with: $0 logs"
        fi
        ;;
    
    stop)
        echo "🛑 Stopping Stock Screener..."
        sudo systemctl stop stockscreener.service
        echo "✅ Stock Screener stopped."
        ;;
    
    restart)
        echo "🔄 Restarting Stock Screener..."
        sudo systemctl restart stockscreener.service
        sleep 2
        if sudo systemctl is-active --quiet stockscreener.service; then
            echo "✅ Stock Screener restarted successfully!"
            show_url
        else
            echo "❌ Failed to restart. Check logs with: $0 logs"
        fi
        ;;
    
    status)
        echo "📊 Stock Screener Status:"
        sudo systemctl status stockscreener.service --no-pager
        echo ""
        if sudo systemctl is-active --quiet stockscreener.service; then
            show_url
        fi
        ;;
    
    logs)
        echo "📋 Stock Screener Logs (Press Ctrl+C to exit):"
        sudo journalctl -u stockscreener.service -f
        ;;
    
    enable)
        echo "⚡ Enabling auto-start on boot..."
        sudo systemctl enable stockscreener.service
        echo "✅ Stock Screener will now start automatically on boot!"
        ;;
    
    disable)
        echo "🚫 Disabling auto-start on boot..."
        sudo systemctl disable stockscreener.service
        echo "✅ Auto-start disabled."
        ;;
    
    install)
        echo "📦 Installing Stock Screener service..."
        if [ -f "./setup_autostart.sh" ]; then
            chmod +x setup_autostart.sh
            ./setup_autostart.sh
        else
            echo "❌ setup_autostart.sh not found in current directory"
            echo "Make sure you're in the stockscreener directory"
        fi
        ;;
    
    uninstall)
        echo "🗑️ Removing Stock Screener service..."
        sudo systemctl stop stockscreener.service 2>/dev/null
        sudo systemctl disable stockscreener.service 2>/dev/null
        sudo rm -f /etc/systemd/system/stockscreener.service
        sudo systemctl daemon-reload
        echo "✅ Stock Screener service removed."
        ;;
    
    url)
        show_url
        ;;
    
    *)
        show_help
        ;;
esac