#!/bin/bash

# Script to prepare the application for deployment to Azure

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Preparing Expense Tracker for deployment to Azure...${NC}"

# Check if az CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}Azure CLI is not installed. Please install it first.${NC}"
    echo "Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Create a deployment directory
echo "Creating deployment package..."
DEPLOY_DIR="deployment"
mkdir -p $DEPLOY_DIR

# Copy necessary files
cp -r app.py requirements.txt templates static $DEPLOY_DIR/

# Create a simple startup script for Azure
echo "Creating startup script for Azure..."
cat > $DEPLOY_DIR/startup.txt << EOL
gunicorn --bind=0.0.0.0 --timeout 600 app:app
EOL

# Create .deployment file for Azure
echo "Creating .deployment file..."
cat > $DEPLOY_DIR/.deployment << EOL
[config]
SCM_DO_BUILD_DURING_DEPLOYMENT=true
EOL

# Create requirements.txt with additional Azure-specific dependencies
echo "Updating requirements.txt with Azure-specific dependencies..."
cat > $DEPLOY_DIR/requirements.txt << EOL
$(cat requirements.txt)
gunicorn==20.1.0
EOL

# ZIP the deployment package
echo "Creating ZIP deployment package..."
cd $DEPLOY_DIR && zip -r ../expense-tracker-azure-deployment.zip . && cd ..

echo -e "${GREEN}Deployment package created: expense-tracker-azure-deployment.zip${NC}"
echo -e "${BLUE}To deploy to Azure, use one of the following methods:${NC}"
echo -e "1. Use the Azure portal to deploy the ZIP file"
echo -e "2. Use Azure CLI: az webapp deployment source config-zip --resource-group <group-name> --name <app-name> --src expense-tracker-azure-deployment.zip"
echo -e "3. Use the GitHub Actions workflow we've set up in your repository"

echo -e "\n${YELLOW}Note: Make sure to configure the following in your Azure Web App:${NC}"
echo -e "- Python version: 3.10 or higher"
echo -e "- Startup command from startup.txt"
