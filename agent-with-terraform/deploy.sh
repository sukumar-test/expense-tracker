#!/bin/bash

# Script to deploy the AWS architecture using Terraform

echo "Starting deployment process..."

# 1. Package Lambda functions
echo "Packaging Lambda functions..."
./package-lambdas.sh

# 2. Initialize Terraform (if not already done)
echo "Initializing Terraform..."
terraform init

# 3. Validate the configuration
echo "Validating Terraform configuration..."
terraform validate
if [ $? -ne 0 ]; then
  echo "Terraform validation failed. Please fix the issues and try again."
  exit 1
fi

# 4. Plan the deployment
echo "Planning Terraform deployment..."
terraform plan -out=tfplan

# 5. Apply the configuration (with confirmation)
echo ""
echo "Ready to deploy the infrastructure."
read -p "Continue with deployment? (y/n): " confirm
if [[ $confirm =~ ^[Yy]$ ]]; then
  echo "Applying Terraform configuration..."
  terraform apply tfplan
  
  if [ $? -eq 0 ]; then
    echo ""
    echo "Deployment completed successfully."
    echo ""
    echo "API Gateway endpoint:"
    terraform output api_endpoint
    echo ""
    echo "Other resources:"
    terraform output
  else
    echo "Deployment failed."
  fi
else
  echo "Deployment cancelled."
fi
