#!/bin/bash

# setup_https.sh - Setup HTTPS for Stock Screener with Nginx and Let's Encrypt

echo "🔒 Setting up HTTPS for Stock Screener..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Nginx
echo "🌐 Installing Nginx..."
sudo apt install nginx -y

# Install Certbot for Let's Encrypt
echo "🔐 Installing Certbot..."
sudo apt install certbot python3-certbot-nginx -y

# Create Nginx configuration
echo "⚙️ Creating Nginx configuration..."
sudo tee /etc/nginx/sites-available/stockscreener << 'EOF'
server {
    listen 80;
    server_name YOUR_DOMAIN_HERE;  # Replace with your domain
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # WebSocket support for Streamlit
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Forwarded-Server $host;
    }
}
EOF

# Enable the site
echo "✅ Enabling Nginx site..."
sudo ln -sf /etc/nginx/sites-available/stockscreener /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
sudo nginx -t

# Start and enable Nginx
echo "🚀 Starting Nginx..."
sudo systemctl start nginx
sudo systemctl enable nginx

echo "✅ Nginx setup complete!"
echo ""
echo "🔐 Next steps:"
echo "1. Replace YOUR_DOMAIN_HERE in /etc/nginx/sites-available/stockscreener with your actual domain"
echo "2. Run: sudo certbot --nginx -d yourdomain.com"
echo "3. Start your Streamlit app: streamlit run clean_app.py --server.port 8501"
echo ""
echo "📝 Manual steps required:"
echo "sudo nano /etc/nginx/sites-available/stockscreener"
echo "# Replace YOUR_DOMAIN_HERE with your domain"
echo "sudo systemctl reload nginx"
echo "sudo certbot --nginx -d yourdomain.com"