#!/bin/bash

# update_server.sh - Automated server update script for Enhanced Stock Screener
# This script updates the server with the latest projection features

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Header
echo -e "${BLUE}"
echo "🚀 Enhanced Stock Screener - Server Update Script"
echo "=================================================="
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -f "enhanced_app.py" ]; then
    error "Not in the stockscreener directory. Please run this script from the project root."
    echo "Expected files: enhanced_app.py, requirements.txt"
    exit 1
fi

log "Starting server update process..."

# Step 1: Stop existing service
log "Step 1: Stopping existing service..."
if systemctl is-active --quiet stockscreener 2>/dev/null; then
    log "Stopping systemd service..."
    sudo systemctl stop stockscreener
    success "Service stopped"
elif [ -f "./manage_stockscreener.sh" ]; then
    log "Using management script to stop service..."
    ./manage_stockscreener.sh stop
    success "Service stopped via management script"
else
    warning "No running service detected"
fi

# Step 2: Backup current version
log "Step 2: Creating backup..."
BACKUP_NAME="stockscreener-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czf "../$BACKUP_NAME" . --exclude='.git' --exclude='__pycache__' --exclude='*.pyc'
success "Backup created: ../$BACKUP_NAME"

# Step 3: Pull latest changes
log "Step 3: Pulling latest changes from git..."
git fetch origin
CURRENT_COMMIT=$(git rev-parse HEAD)
LATEST_COMMIT=$(git rev-parse origin/main)

if [ "$CURRENT_COMMIT" = "$LATEST_COMMIT" ]; then
    success "Already up to date"
else
    log "Updating from $CURRENT_COMMIT to $LATEST_COMMIT"
    git pull origin main
    success "Git pull completed"
fi

# Step 4: Check for new files
log "Step 4: Verifying new projection features..."
NEW_FILES=(
    "test_projection.py"
    "technical_projection_ui.py" 
    "PROJECTION_FEATURE_GUIDE.md"
    ".kiro/steering/product.md"
    ".kiro/steering/tech.md"
    ".kiro/steering/structure.md"
)

for file in "${NEW_FILES[@]}"; do
    if [ -f "$file" ]; then
        success "Found: $file"
    else
        warning "Missing: $file (may not be critical)"
    fi
done

# Step 5: Update dependencies
log "Step 5: Updating Python dependencies..."
pip3 install --user --upgrade pip
pip3 install --user -r requirements.txt

# Verify critical packages
log "Verifying critical packages..."
python3 -c "
import sys
packages = ['streamlit', 'yfinance', 'plotly', 'pandas', 'numpy', 'scikit-learn']
missing = []
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg}')
    except ImportError:
        missing.append(pkg)
        print(f'❌ {pkg}')

if missing:
    print(f'Missing packages: {missing}')
    sys.exit(1)
else:
    print('🎉 All critical packages available!')
"

success "Dependencies updated successfully"

# Step 6: Test new projection features
log "Step 6: Testing new projection features..."
if python3 test_projection.py > /tmp/projection_test.log 2>&1; then
    success "Projection features test passed"
else
    error "Projection features test failed"
    echo "Test log:"
    cat /tmp/projection_test.log
    warning "Continuing with update, but projection features may not work properly"
fi

# Step 7: Update configuration files
log "Step 7: Checking configuration..."

# Check if .env file exists, create example if not
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    log "Creating .env file from example..."
    cp .env.example .env
    warning "Please edit .env file to add your API keys (optional)"
fi

# Step 8: Restart service
log "Step 8: Restarting service..."
if systemctl list-unit-files | grep -q stockscreener; then
    log "Starting systemd service..."
    sudo systemctl start stockscreener
    sleep 3
    if systemctl is-active --quiet stockscreener; then
        success "Systemd service started successfully"
    else
        error "Failed to start systemd service"
        log "Checking service logs..."
        sudo journalctl -u stockscreener --no-pager -n 20
    fi
elif [ -f "./manage_stockscreener.sh" ]; then
    log "Starting service via management script..."
    ./manage_stockscreener.sh start
    sleep 3
    ./manage_stockscreener.sh status
else
    warning "No service management found. You may need to start manually:"
    echo "  streamlit run enhanced_app.py --server.port 8501 --server.address 0.0.0.0"
fi

# Step 9: Verify update
log "Step 9: Verifying update..."

# Check if service is responding
if command -v curl >/dev/null 2>&1; then
    log "Testing web interface..."
    if curl -s -I http://localhost:8501 | grep -q "200 OK"; then
        success "Web interface is responding"
    else
        warning "Web interface may not be ready yet (this is normal, give it a minute)"
    fi
fi

# Step 10: Display access information
log "Step 10: Update complete!"

echo -e "\n${GREEN}🎉 Server Update Successful!${NC}"
echo -e "${BLUE}=================================================${NC}"

# Get server IP
if command -v curl >/dev/null 2>&1; then
    EXTERNAL_IP=$(curl -s ifconfig.me 2>/dev/null || echo "Unable to detect")
    echo -e "🌐 External Access: ${GREEN}http://$EXTERNAL_IP:8501${NC}"
fi

echo -e "🏠 Local Access: ${GREEN}http://localhost:8501${NC}"

echo -e "\n${YELLOW}📈 New Features Available:${NC}"
echo "• Interactive 30-day price projections"
echo "• 5 advanced projection algorithms"
echo "• AI-powered trading insights"
echo "• Enhanced technical analysis charts"
echo "• Pattern recognition and volume analysis"

echo -e "\n${YELLOW}📖 Documentation:${NC}"
echo "• Feature Guide: PROJECTION_FEATURE_GUIDE.md"
echo "• Test Suite: python3 test_projection.py"
echo "• Server Commands: SERVER_UPDATE_COMMANDS.md"

if [ -f "./manage_stockscreener.sh" ]; then
    echo -e "\n${YELLOW}🔧 Management Commands:${NC}"
    echo "• Status: ./manage_stockscreener.sh status"
    echo "• Logs: ./manage_stockscreener.sh logs"
    echo "• Restart: ./manage_stockscreener.sh restart"
    echo "• URL: ./manage_stockscreener.sh url"
fi

echo -e "\n${BLUE}⚠️ Important Notes:${NC}"
echo "• Backup created: ../$BACKUP_NAME"
echo "• Test the new projection features in Technical Analysis step"
echo "• Use the projection slider (1-30 days) for price forecasting"
echo "• Check logs if you encounter any issues"

echo -e "\n${GREEN}Happy Trading! 📊${NC}"

# Optional: Show service status
if [ -f "./manage_stockscreener.sh" ]; then
    echo -e "\n${BLUE}Current Service Status:${NC}"
    ./manage_stockscreener.sh status
fi