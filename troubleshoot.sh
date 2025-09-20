#!/bin/bash

# 🔧 Enhanced Stock Screener - Troubleshooting Script

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Enhanced Stock Screener - Troubleshooting${NC}"
echo "=============================================="

# Check system resources
echo -e "\n${BLUE}📊 System Resources:${NC}"
echo "Memory usage:"
free -h
echo -e "\nDisk usage:"
df -h /
echo -e "\nCPU load:"
uptime

# Check service status
echo -e "\n${BLUE}🔍 Service Status:${NC}"
if sudo systemctl is-active --quiet stockscreener; then
    echo -e "${GREEN}✅ Stock Screener service: RUNNING${NC}"
else
    echo -e "${RED}❌ Stock Screener service: NOT RUNNING${NC}"
fi

if sudo systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✅ Nginx service: RUNNING${NC}"
else
    echo -e "${RED}❌ Nginx service: NOT RUNNING${NC}"
fi

# Check ports
echo -e "\n${BLUE}🌐 Port Status:${NC}"
if netstat -tuln | grep -q ":8501"; then
    echo -e "${GREEN}✅ Port 8501 (Streamlit): LISTENING${NC}"
else
    echo -e "${RED}❌ Port 8501 (Streamlit): NOT LISTENING${NC}"
fi

if netstat -tuln | grep -q ":80"; then
    echo -e "${GREEN}✅ Port 80 (HTTP): LISTENING${NC}"
else
    echo -e "${RED}❌ Port 80 (HTTP): NOT LISTENING${NC}"
fi

# Check recent logs
echo -e "\n${BLUE}📝 Recent Logs (last 10 lines):${NC}"
sudo journalctl -u stockscreener --no-pager -n 10

# Check Python packages
echo -e "\n${BLUE}🐍 Python Environment:${NC}"
python3 --version
echo "Streamlit version:"
/home/ubuntu/.local/bin/streamlit --version 2>/dev/null || echo "Streamlit not found in PATH"

# Check repository status
echo -e "\n${BLUE}📁 Repository Status:${NC}"
if [ -d "/home/ubuntu/stockscreener" ]; then
    cd /home/ubuntu/stockscreener
    echo "Repository exists"
    echo "Last commit:"
    git log --oneline -1 2>/dev/null || echo "Git log unavailable"
    echo "Current branch:"
    git branch --show-current 2>/dev/null || echo "Git branch unavailable"
else
    echo -e "${RED}❌ Repository not found at /home/ubuntu/stockscreener${NC}"
fi

# Check environment file
echo -e "\n${BLUE}🔑 Environment Configuration:${NC}"
if [ -f "/home/ubuntu/stockscreener/.env" ]; then
    echo -e "${GREEN}✅ .env file exists${NC}"
    echo "Environment variables:"
    grep -v "^#" /home/ubuntu/stockscreener/.env | grep -v "^$" | sed 's/=.*/=***/' || echo "No variables found"
else
    echo -e "${RED}❌ .env file not found${NC}"
fi

# Network connectivity test
echo -e "\n${BLUE}🌐 Network Connectivity:${NC}"
if curl -s --connect-timeout 5 https://api.github.com > /dev/null; then
    echo -e "${GREEN}✅ Internet connectivity: OK${NC}"
else
    echo -e "${RED}❌ Internet connectivity: FAILED${NC}"
fi

# Get server IP
SERVER_IP=$(curl -s --connect-timeout 5 ifconfig.me 2>/dev/null || echo "Unable to detect")
echo "Server IP: $SERVER_IP"

# Quick fixes section
echo -e "\n${YELLOW}🔧 Quick Fixes:${NC}"
echo "1. Restart services:"
echo "   sudo systemctl restart stockscreener nginx"
echo ""
echo "2. Check detailed logs:"
echo "   sudo journalctl -u stockscreener -f"
echo ""
echo "3. Update application:"
echo "   cd ~/stockscreener && git pull && sudo systemctl restart stockscreener"
echo ""
echo "4. Reinstall (if needed):"
echo "   curl -sSL https://raw.githubusercontent.com/jaspalkahlon/stockscreener/main/install_server.sh | bash"
echo ""
echo "5. Check firewall:"
echo "   sudo ufw status"
echo ""

# Test local connection
echo -e "\n${BLUE}🧪 Testing Local Connection:${NC}"
if curl -s --connect-timeout 10 http://localhost:8501 > /dev/null; then
    echo -e "${GREEN}✅ Local Streamlit connection: OK${NC}"
else
    echo -e "${RED}❌ Local Streamlit connection: FAILED${NC}"
    echo "Try restarting the service: sudo systemctl restart stockscreener"
fi

echo -e "\n${GREEN}🎯 Troubleshooting complete!${NC}"
echo "If issues persist, check the logs with: sudo journalctl -u stockscreener -f"