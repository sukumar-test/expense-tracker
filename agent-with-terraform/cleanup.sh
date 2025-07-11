#!/bin/bash

# Script to clean up resources created by Terraform

echo "This script will destroy all resources created by Terraform."
echo "This action is IRREVERSIBLE!"
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
  echo "Cleanup cancelled."
  exit 0
fi

echo "Proceeding with resource destruction..."
terraform destroy

if [ $? -eq 0 ]; then
  echo "All resources have been destroyed successfully."
else
  echo "Resource destruction failed. Please check the error messages above."
fi
