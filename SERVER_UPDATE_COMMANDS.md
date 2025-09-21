# 🚀 Server Update Commands - Technical Analysis Projections

## 📋 Quick Update Commands

### For Existing Servers (Recommended)
```bash
# 1. Navigate to your project directory
cd ~/stockscreener  # or wherever your project is located

# 2. Stop the current service (if running)
sudo systemctl stop stockscreener
# OR if using the management script:
./manage_stockscreener.sh stop

# 3. Pull the latest changes
git pull origin main

# 4. Install any new dependencies (if needed)
pip3 install --user -r requirements.txt

# 5. Test the new projection feature
python3 test_projection.py

# 6. Restart the service
sudo systemctl start stockscreener
# OR using management script:
./manage_stockscreener.sh start

# 7. Check status
./manage_stockscreener.sh status
```

### For Google Cloud VM (One-liner)
```bash
curl -sSL https://raw.githubusercontent.com/jaspalkahlon/stockscreener/main/update_server.sh | bash
```

## 🔧 Detailed Update Process

### Step 1: Connect to Your Server
```bash
# SSH into your server
ssh username@your-server-ip

# Or for Google Cloud VM:
gcloud compute ssh your-vm-name --zone=your-zone
```

### Step 2: Navigate and Update
```bash
# Go to project directory
cd ~/stockscreener

# Check current status
git status
git log --oneline -5

# Pull latest changes
git pull origin main

# Verify new files are present
ls -la *.py | grep -E "(projection|technical)"
```

### Step 3: Update Dependencies
```bash
# Update pip packages
pip3 install --user --upgrade pip
pip3 install --user -r requirements.txt

# Verify critical packages
python3 -c "import plotly, sklearn, scipy; print('✅ All packages OK')"
```

### Step 4: Test New Features
```bash
# Run the projection test suite
python3 test_projection.py

# Expected output should show:
# ✅ All required dependencies are available!
# ✅ Projection chart created successfully
# 🎉 ALL TESTS PASSED!
```

### Step 5: Restart Services
```bash
# Using systemctl (if configured)
sudo systemctl stop stockscreener
sudo systemctl start stockscreener
sudo systemctl status stockscreener

# OR using management script
./manage_stockscreener.sh restart
./manage_stockscreener.sh status
```

### Step 6: Verify Update
```bash
# Check if service is running
./manage_stockscreener.sh url

# Test the web interface
curl -I http://localhost:8501

# Check logs for any errors
./manage_stockscreener.sh logs
```

## 🆕 New Features Available After Update

### 1. Enhanced Technical Analysis
- **30-day projection slider** in Technical Analysis step
- **5 projection methods**: Trend, MA, S/R, Volatility, Ensemble
- **Interactive charts** with confidence bands

### 2. AI Trading Insights
- **Overbought/Oversold signals** based on RSI
- **Trend strength indicators** with ADX
- **Volume breakout detection**
- **Support/Resistance proximity alerts**

### 3. Advanced Visualizations
- **Multi-subplot charts** with technical overlays
- **Projection confidence bands** for each method
- **Pattern recognition** display
- **Volume analysis** integration

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Issue: "Could not fetch data"
```bash
# Check internet connectivity
ping -c 3 finance.yahoo.com

# Verify yfinance is working
python3 -c "import yfinance as yf; print(yf.Ticker('RELIANCE.NS').info['shortName'])"
```

#### Issue: "Projection chart creation failed"
```bash
# Check plotly installation
python3 -c "import plotly.graph_objects as go; print('Plotly OK')"

# Reinstall if needed
pip3 install --user --upgrade plotly
```

#### Issue: Service won't start
```bash
# Check for port conflicts
sudo netstat -tlnp | grep :8501

# Check service logs
journalctl -u stockscreener -f

# Or check application logs
./manage_stockscreener.sh logs
```

#### Issue: Missing dependencies
```bash
# Install missing packages
pip3 install --user scipy scikit-learn plotly

# For TA-Lib (optional)
sudo apt-get update
sudo apt-get install -y build-essential
pip3 install --user TA-Lib
```

## 📊 Performance Optimization

### For Better Performance
```bash
# Increase memory if needed (Google Cloud)
gcloud compute instances set-machine-type your-vm-name \
    --machine-type=e2-standard-2 --zone=your-zone

# Restart VM after machine type change
gcloud compute instances stop your-vm-name --zone=your-zone
gcloud compute instances start your-vm-name --zone=your-zone
```

### Memory Usage Optimization
```bash
# Add to ~/.bashrc for better Python performance
echo 'export PYTHONUNBUFFERED=1' >> ~/.bashrc
echo 'export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200' >> ~/.bashrc
source ~/.bashrc
```

## 🔐 Security Updates

### Firewall Rules (if needed)
```bash
# For Google Cloud VM
gcloud compute firewall-rules create allow-stockscreener \
    --allow tcp:8501 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow Stock Screener access"
```

### SSL/HTTPS (optional)
```bash
# If you want to enable HTTPS
./setup_https.sh

# Or use Cloudflare tunnel
./setup_cloudflare_tunnel.sh
```

## 📈 Usage After Update

### Access the New Features
1. **Open your browser** and go to your server URL
2. **Navigate to Technical Analysis** (Step 4)
3. **Select a stock** from your analyzed list
4. **Use the projection slider** (1-30 days)
5. **Click "Analyze with Projections"**
6. **Explore different projection methods** in the options panel

### Example URL
```
http://your-server-ip:8501
```

## 📞 Support Commands

### Get System Information
```bash
# System info
uname -a
python3 --version
pip3 --version

# Disk space
df -h

# Memory usage
free -h

# Service status
systemctl status stockscreener
```

### Backup Before Update (Recommended)
```bash
# Create backup
tar -czf stockscreener-backup-$(date +%Y%m%d).tar.gz ~/stockscreener

# List backups
ls -la ~/stockscreener-backup-*.tar.gz
```

### Rollback if Needed
```bash
# Go back to previous version
cd ~/stockscreener
git log --oneline -10
git checkout <previous-commit-hash>

# Restart service
./manage_stockscreener.sh restart
```

---

## 🎉 Update Complete!

After running these commands, your Enhanced Indian Stock Screener will have:

✅ **Interactive 30-day price projections**  
✅ **5 advanced projection algorithms**  
✅ **AI-powered trading insights**  
✅ **Professional interactive charts**  
✅ **Enhanced technical analysis capabilities**  

**Happy Trading! 📈**

---

*For issues or questions, check the logs with `./manage_stockscreener.sh logs` or run the test suite with `python3 test_projection.py`*