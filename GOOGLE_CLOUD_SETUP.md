# 🌐 Google Cloud Setup Guide - Enhanced Stock Screener

## 🎯 **Why Google Cloud?**
- ✅ **$300 FREE Credits** (12 months)
- ✅ **Easy Setup**: More straightforward than Oracle
- ✅ **Reliable**: 99.9% uptime
- ✅ **Fast**: Global network
- ✅ **Beginner Friendly**: Great interface

**💰 Cost: FREE for 12 months, then ~$5-8/month**

---

## 📋 **Step-by-Step Setup (15 minutes)**

### **Step 1: Create Google Cloud Account**

1. **Go to**: https://cloud.google.com/
2. **Click**: "Get started for free"
3. **Sign in** with your Google account (or create one)
4. **Accept terms** and **verify phone number**
5. **Add payment method** (required but won't be charged during free trial)
6. **Get $300 free credits** ✅

### **Step 2: Create Your Virtual Machine**

1. **Go to**: Console → Compute Engine → VM instances
2. **Click**: "Create Instance"
3. **Configure**:
   - **Name**: `stock-screener-vm`
   - **Region**: Choose closest to you (e.g., `us-central1`)
   - **Zone**: Any (e.g., `us-central1-a`)
   - **Machine type**: 
     - **Series**: E2
     - **Machine type**: `e2-small` (2 vCPU, 2GB RAM) - Perfect for stock screener
   - **Boot disk**: 
     - **Operating System**: Ubuntu
     - **Version**: Ubuntu 22.04 LTS
     - **Size**: 20 GB (more than enough)
   - **Firewall**: 
     - ✅ **Check**: "Allow HTTP traffic"
     - ✅ **Check**: "Allow HTTPS traffic"

4. **Click**: "Create" (takes 1-2 minutes)

### **Step 3: Connect to Your Server**

**Option A: Browser SSH (Easiest)**
1. **Click**: "SSH" button next to your VM instance
2. **Browser window opens** with terminal - you're connected! ✅

**Option B: Local Terminal (Mac/Linux)**
1. **Install gcloud CLI**: https://cloud.google.com/sdk/docs/install
2. **Run**: `gcloud compute ssh stock-screener-vm --zone=us-central1-a`

### **Step 4: One-Click Installation**

**Copy and paste this entire command in your SSH terminal:**

```bash
curl -sSL https://raw.githubusercontent.com/jaspalkahlon/stockscreener/main/install_server.sh | bash
```

**That's it!** The script will:
- Install all dependencies
- Download your stock screener
- Configure auto-start
- Set up web server
- Configure firewall

**⏱️ Takes 3-5 minutes to complete**

### **Step 5: Configure Firewall (Important!)**

1. **Go to**: VPC Network → Firewall
2. **Click**: "Create Firewall Rule"
3. **Configure**:
   - **Name**: `allow-streamlit`
   - **Direction**: Ingress
   - **Action**: Allow
   - **Targets**: All instances in the network
   - **Source IP ranges**: `0.0.0.0/0`
   - **Protocols and ports**: 
     - ✅ **TCP**
     - **Ports**: `8501`
4. **Click**: "Create"

### **Step 6: Access Your Stock Screener**

1. **Go back to**: Compute Engine → VM instances
2. **Find your VM's External IP** (e.g., `34.123.45.67`)
3. **Open browser** and go to: `http://YOUR_EXTERNAL_IP`
4. **🎉 Your enhanced stock screener is live!**

---

## 🔧 **Management & Monitoring**

### **Check Status:**
```bash
# SSH into your VM and run:
sudo systemctl status stockscreener
```

### **View Logs:**
```bash
sudo journalctl -u stockscreener -f
```

### **Restart Service:**
```bash
sudo systemctl restart stockscreener
```

### **Update Code:**
```bash
cd ~/stockscreener
git pull
sudo systemctl restart stockscreener
```

---

## 💰 **Cost Management**

### **Free Tier Usage:**
- **$300 credits** last 12+ months for this setup
- **e2-small instance**: ~$13/month (covered by credits)
- **20GB disk**: ~$0.80/month
- **Network**: Minimal cost

### **After Free Tier:**
- **Total cost**: ~$5-8/month
- **Much cheaper than**: Render ($7), Heroku ($25), AWS ($15+)

### **Cost Optimization Tips:**
1. **Stop VM when not needed**: Compute Engine → Stop
2. **Use preemptible instances**: 80% cheaper (may restart occasionally)
3. **Monitor usage**: Billing → Reports

---

## 🛡️ **Security Best Practices**

### **Automatic Updates:**
```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### **Firewall:**
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow 8501
```

### **SSL Certificate (Optional):**
```bash
# If you want HTTPS
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx
```

---

## 🚨 **Troubleshooting**

### **Can't access from browser:**
1. **Check External IP**: Make sure you're using the right IP
2. **Check firewall rule**: Ensure port 8501 is allowed
3. **Check service**: `sudo systemctl status stockscreener`

### **Service not running:**
```bash
# Check logs
sudo journalctl -u stockscreener -n 20

# Restart service
sudo systemctl restart stockscreener

# Check if port is listening
sudo netstat -tuln | grep 8501
```

### **Out of memory:**
```bash
# Check memory usage
free -h

# If needed, upgrade to e2-medium (4GB RAM)
```

### **Run troubleshooting script:**
```bash
curl -sSL https://raw.githubusercontent.com/jaspalkahlon/stockscreener/main/troubleshoot.sh | bash
```

---

## 🔄 **Backup & Maintenance**

### **Create VM Snapshot:**
1. **Go to**: Compute Engine → Snapshots
2. **Click**: "Create Snapshot"
3. **Select**: Your VM disk
4. **Name**: `stock-screener-backup-YYYYMMDD`

### **Auto-backup Script:**
```bash
# Create weekly backup
gcloud compute disks snapshot stock-screener-vm --zone=us-central1-a --snapshot-names=weekly-backup-$(date +%Y%m%d)
```

---

## 📱 **Mobile & Remote Access**

### **Mobile Optimization:**
- Your stock screener is fully mobile-responsive
- Works perfectly on phones and tablets
- Bookmark `http://YOUR_IP` for quick access

### **Share with Others:**
- Send them your VM's external IP
- Multiple users can access simultaneously
- Each user gets their own session

---

## 🌟 **Advanced Features**

### **Custom Domain (Optional):**
1. **Buy domain** (e.g., from Google Domains)
2. **Point A record** to your VM's external IP
3. **Access via**: `http://yourdomain.com`

### **HTTPS Setup:**
```bash
# After setting up domain
sudo certbot --nginx -d yourdomain.com
```

### **Auto-scaling (Advanced):**
- Use Google Cloud Load Balancer
- Create instance template
- Set up auto-scaling group

---

## 🎯 **Why This Setup is Perfect**

✅ **Reliable**: Google's infrastructure
✅ **Fast**: Global CDN and fast SSDs
✅ **Scalable**: Easy to upgrade resources
✅ **Monitored**: Built-in monitoring and alerts
✅ **Secure**: Google's security standards
✅ **Supported**: Excellent documentation and support

---

## 📞 **Getting Help**

### **Google Cloud Support:**
- **Free tier**: Community support
- **Paid plans**: 24/7 technical support

### **Stock Screener Issues:**
1. **Check logs**: `sudo journalctl -u stockscreener -f`
2. **Run troubleshoot script**: Available in your repository
3. **GitHub Issues**: Open issue in your repository

---

## 🎉 **Success Checklist**

- ✅ Google Cloud account created
- ✅ VM instance running
- ✅ Firewall rules configured
- ✅ Stock screener installed
- ✅ Accessible via browser
- ✅ Auto-start enabled
- ✅ Monitoring set up

**🌟 Your professional stock screener is now running 24/7 on Google Cloud!**

**Access it at**: `http://YOUR_VM_EXTERNAL_IP`

---

## 💡 **Pro Tips**

1. **Bookmark your IP** for quick access
2. **Set up billing alerts** to monitor costs
3. **Create snapshots** before major updates
4. **Use labels** to organize resources
5. **Monitor performance** via Google Cloud Console

**🚀 Enjoy your professional-grade stock analysis platform!**