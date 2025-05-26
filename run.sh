#!/bin/bash

# This script helps set up and run the Expense Tracker application

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up Expense Tracker...${NC}"

# Check if virtual environment exists, create if it doesn't
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo -e "${GREEN}Setup complete!${NC}"
echo -e "${GREEN}Starting Expense Tracker application...${NC}"

# Run the Flask application
python app.py
