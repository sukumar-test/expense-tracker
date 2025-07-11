#!/bin/bash

# Script to package Lambda functions for deployment

# Create dist directory if it doesn't exist
mkdir -p lambda/dist

# Change to lambda directory
cd lambda

# Install dependencies (if you have any)
# npm init -y
# npm install aws-sdk

# Package each Lambda function
echo "Packaging main Lambda function..."
zip -r dist/main-function.zip main-function.js

echo "Packaging authorizer Lambda function..."
zip -r dist/authorizer-function.zip authorizer-function.js

echo "Packaging consumer Lambda function..."
zip -r dist/consumer-function.zip consumer-function.js

# Return to project root
cd ..

echo "Lambda functions packaged successfully. Update your terraform.tfvars file with the following paths:"
echo "lambda_zip_path = \"lambda/dist/main-function.zip\""
echo "authorizer_zip_path = \"lambda/dist/authorizer-function.zip\""
echo "consumer_zip_path = \"lambda/dist/consumer-function.zip\""
