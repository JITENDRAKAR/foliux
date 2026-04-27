#!/bin/bash

# ================================================================= #
# FOLIUX VPS DEPLOYMENT SCRIPT (Ubuntu)                             #
# ================================================================= #

# Configuration - Update these to match your VPS settings
PROJECT_DIR="/home/foliux"
VENV_PATH="$PROJECT_DIR/venv"
SERVICE_NAME="foliux"  # Name of your systemd service file (e.g., foliux.service)

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Deployment to Foliux...${NC}"

# Navigate to project directory
cd $PROJECT_DIR || { echo "❌ Directory $PROJECT_DIR not found"; exit 1; }

# 1. Pull latest changes
echo -e "${BLUE}📥 Pulling latest changes from Git...${NC}"
git pull foliux main

# 2. Clear Python Cache (__pycache__)
echo -e "${BLUE}🧹 Clearing Python bytecode cache...${NC}"
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# 3. Activate virtual environment
if [ -d "$VENV_PATH" ]; then
    echo -e "${BLUE}🐍 Activating virtual environment...${NC}"
    source "$VENV_PATH/bin/activate"
else
    echo -e "⚠️ Virtual environment not found at $VENV_PATH"
fi

# 4. Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip install -r requirements.txt

# 5. Run database migrations
echo -e "${BLUE}⚙️ Running database migrations...${NC}"
python manage.py migrate --noinput

# 6. Collect static files
echo -e "${BLUE}🎨 Collecting static files...${NC}"
python manage.py collectstatic --noinput

# 7. Restart the application service
echo -e "${BLUE}🔄 Restarting application service ($SERVICE_NAME)...${NC}"
if command -v systemctl >/dev/null 2>&1; then
    sudo systemctl daemon-reload
    sudo systemctl restart $SERVICE_NAME
    
    # Verify if service is running
    if systemctl is-active --quiet $SERVICE_NAME; then
        echo -e "${GREEN}✅ Service $SERVICE_NAME is active.${NC}"
    else
        echo -e "❌ Service $SERVICE_NAME failed to start. Check logs with: journalctl -u $SERVICE_NAME"
        exit 1
    fi
else
    echo -e "⚠️ systemctl not found. Please restart your web server manually (e.g., Gunicorn/Nginx)."
fi

# 8. Success Summary
DEPLOY_TIME=$(date '+%Y-%m-%d %H:%M:%S')
VERSION=$(git rev-parse --short HEAD)
echo -e "\n${GREEN}==============================================${NC}"
echo -e "${GREEN}✨ DEPLOYMENT SUCCESSFUL!${NC}"
echo -e "${GREEN}==============================================${NC}"
echo -e "${BLUE}🕒 Time: ${NC}$DEPLOY_TIME"
echo -e "${BLUE}🔢 Version: ${NC}$VERSION"
echo -e "${BLUE}🔗 Repository: ${NC}https://github.com/JITENDRAKAR/foliux"
echo -e "${BLUE}🌐 Live Site: ${NC}https://npits.in"
echo -e "${GREEN}==============================================${NC}\n"
