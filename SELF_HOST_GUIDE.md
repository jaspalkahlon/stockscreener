# 🏠 Self-Hosting Guide: Enhanced Stock Screener

## 🎯 **Oracle Cloud Free Tier Setup (RECOMMENDED)**

### **Why Oracle Cloud?**
- ✅ **100% FREE Forever** (not a trial)
- ✅ **Powerful**: 1-4 ARM CPUs + 6-24GB RAM
- ✅ **Always On**: 24/7 availability
- ✅ **No Credit Card Charges**: Truly free tier
- ✅ **Perfect for Stock Screener**: More than enough resources

---

## 📋 **Step-by-Step Setup (Non-Techie Friendly)**

### **Step 1: Create Oracle Cloud Account**

1. **Go to**: https://oracle.com/cloud/free
2. **Click**: "Start for free"
3. **Fill in details**:
   - Country: Your country
   - Name: Your name
   - Email: Your email
   - Create password
4. **Verify email** and **phone number**
5. **Complete signup** (no credit card required for free tier)

### **Step 2: Create Your Server (VM)**

1. **Login** to Oracle Cloud Console
2. **Click**: "Create a VM instance"
3. **Configure**:
   - **Name**: `stock-screener-server`
   - **Image**: `Ubuntu 22.04` (select this)
   - **Shape**: `VM.Standard.A1.Flex` (ARM - FREE)
   - **CPUs**: 2 (or up to 4 if available)
   - **Memory**: 12 GB (or up to 24 GB)
4. **Networking**:
   - Keep default VCN
   - ✅ **Check**: "Assign a public IPv4 address"
5. **SSH Keys**:
   - **Select**: "Generate SSH key pair"
   - **Download** both keys (save them safely!)
6. **Click**: "Create"

**⏱️ Wait 2-3 minutes for server to start**

### **Step 3: Configure Firewall**

1. **Go to**: Networking → Virtual Cloud Networks
2. **Click**: Your VCN name
3. **Click**: "Default Security List"
4. **Click**: "Add Ingress Rules"
5. **Add these rules**:

   **Rule 1 (HTTP):**
   - Source CIDR: `0.0.0.0/0`
   - IP Protocol: `TCP`
   - Destination Port Range: `80`
   
   **Rule 2 (HTTPS):**
   - Source CIDR: `0.0.0.0/0`
   - IP Protocol: `TCP`
   - Destination Port Range: `443`
   
   **Rule 3 (Streamlit):**
   - Source CIDR: `0.0.0.0/0`
   - IP Protocol: `TCP`
   - Destination Port Range: `8501`

6. **Click**: "Add Ingress Rules"

### **Step 4: Connect to Your Server**

**For Mac/Linux:**
1. **Open Terminal**
2. **Run**:
   ```bash
   chmod 600 ~/Downloads/ssh-key-*.key
   ssh -i ~/Downloads/ssh-key-*.key ubuntu@YOUR_SERVER_IP
   ```

**For Windows:**
1. **Download PuTTY**: https://putty.org/
2. **Use your downloaded .ppk key file**
3. **Connect to**: `ubuntu@YOUR_SERVER_IP`

### **Step 5: One-Click Installation Script**

Once connected to your server, **copy and paste this entire script**:

```bash
#!/bin/bash
echo "🚀 Installing Enhanced Stock Screener..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3 python3-pip git nginx

# Install Python packages
pip3 install streamlit yfinance ta plotly pandas python-dotenv requests openpyxl scikit-learn numpy scipy textblob vaderSentiment

# Download NLTK data
python3 -c "import nltk; nltk.download('punkt'); nltk.download('brown')"

# Clone your repository
cd /home/ubuntu
git clone https://github.com/jaspalkahlon/stockscreener.git
cd stockscreener

# Create environment file
cat > .env << EOF
NEWSAPI_KEY=deb95d68a1b94efab22bca49f3f7e7ba
EOF

# Create systemd service for auto-start
sudo tee /etc/systemd/system/stockscreener.service > /dev/null << EOF
[Unit]
Description=Enhanced Stock Screener
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/stockscreener
ExecStart=/usr/local/bin/streamlit run enhanced_app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable stockscreener
sudo systemctl start stockscreener

# Configure Nginx reverse proxy
sudo tee /etc/nginx/sites-available/stockscreener > /dev/null << EOF
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/stockscreener /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

echo "✅ Installation complete!"
echo "🌐 Your stock screener is now available at: http://YOUR_SERVER_IP"
echo "🔧 To check status: sudo systemctl status stockscreener"
echo "📝 To view logs: sudo journalctl -u stockscreener -f"
```

**Just paste this entire script and press Enter!**

### **Step 6: Access Your Stock Screener**

1. **Find your server IP** in Oracle Cloud Console
2. **Open browser** and go to: `http://YOUR_SERVER_IP`
3. **🎉 Your enhanced stock screener is now live!**

---

## 🔧 **Management Commands**

**Check if running:**
```bash
sudo systemctl status stockscreener
```

**Restart service:**
```bash
sudo systemctl restart stockscreener
```

**View logs:**
```bash
sudo journalctl -u stockscreener -f
```

**Update code:**
```bash
cd /home/ubuntu/stockscreener
git pull
sudo systemctl restart stockscreener
```

---

## 💰 **Cost Breakdown**

### **Oracle Cloud Free Tier:**
- **Server**: FREE forever
- **Bandwidth**: 10TB/month FREE
- **Storage**: 200GB FREE
- **Total**: $0/month ✅

### **Alternative Options:**

**Google Cloud:**
- **Free**: $300 credits (12 months)
- **After free tier**: ~$5-10/month

**DigitalOcean:**
- **Basic Droplet**: $4/month
- **CPU Optimized**: $6/month

**AWS:**
- **t2.micro**: FREE for 12 months
- **After free tier**: ~$8-15/month

---

## 🛡️ **Security & Maintenance**

### **Automatic Updates:**
```bash
# Enable automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### **Firewall:**
```bash
# Enable UFW firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow 8501
```

### **SSL Certificate (Optional):**
If you want HTTPS, you can add a free SSL certificate:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx
```

---

## 🚨 **Troubleshooting**

### **Service not starting:**
```bash
sudo journalctl -u stockscreener -n 50
```

### **Can't access from browser:**
1. Check Oracle Cloud security list rules
2. Check server firewall: `sudo ufw status`
3. Check service status: `sudo systemctl status stockscreener`

### **Out of memory:**
```bash
# Check memory usage
free -h
# Restart service
sudo systemctl restart stockscreener
```

---

## 📱 **Mobile Access**

Your stock screener will work perfectly on mobile browsers! Streamlit is responsive and mobile-friendly.

---

## 🔄 **Backup & Updates**

### **Backup your data:**
```bash
# Backup configuration
cp /home/ubuntu/stockscreener/.env ~/backup_env
```

### **Auto-update from GitHub:**
```bash
# Create update script
cat > /home/ubuntu/update_screener.sh << 'EOF'
#!/bin/bash
cd /home/ubuntu/stockscreener
git pull
sudo systemctl restart stockscreener
echo "✅ Stock screener updated!"
EOF

chmod +x /home/ubuntu/update_screener.sh
```

---

## 🎯 **Why This Setup is Perfect for You**

✅ **Zero Technical Knowledge Required**: Copy-paste installation
✅ **Always Online**: 24/7 availability
✅ **Fast Performance**: ARM processors are very efficient
✅ **Free Forever**: Oracle's commitment to free tier
✅ **Scalable**: Can handle multiple users
✅ **Professional**: Your own domain possible
✅ **Secure**: Isolated server environment

**🌟 You'll have a professional stock screener running 24/7 for FREE!**