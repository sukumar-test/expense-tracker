# AWS Data Processing Architecture - Terraform

This repository contains Terraform scripts to deploy a data processing architecture on AWS, as depicted in the architecture diagram.

## Architecture Overview

The architecture consists of the following AWS resources:

1. **API Gateway**: Entry point for the application, secured with a Lambda authorizer
2. **Main Lambda**: Processes the incoming API requests and sends data to Firehose
3. **Authorizer Lambda**: Provides authentication and authorization for API Gateway
4. **Firehose Delivery Stream**: Buffers, transforms, and delivers data to S3
5. **S3 Bucket**: Stores the processed data in a partitioned format (Parquet)
6. **Consumer Lambda**: Processes Firehose records and stores in DynamoDB
7. **DynamoDB Table**: Stores processed data for fast access
8. **AWS Glue**: Provides schema for the data stored in S3

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform >= 1.2.0
- Node.js >= 14.x (for Lambda function development)

## Directory Structure

```
agent-with-terraform/
├── lambda/
│   ├── main-function.js
│   ├── authorizer-function.js
│   └── consumer-function.js
├── main.tf
├── iam.tf
├── variables.tf
├── terraform.tfvars
└── README.md
```

## Deployment Instructions

### 1. Package Lambda Functions

Before deploying with Terraform, you need to package the Lambda functions:

```bash
# Create directories for the zip files
mkdir -p lambda/dist

# Package the main Lambda function
cd lambda
zip -r dist/main-function.zip main-function.js
zip -r dist/authorizer-function.zip authorizer-function.js
zip -r dist/consumer-function.zip consumer-function.js
cd ..
```

### 2. Configure Terraform Variables

Update the `terraform.tfvars` file with your preferred configuration:

```hcl
aws_region   = "us-east-1"
project_name = "data-processing"
environment  = "dev"

tags = {
  Environment = "dev"
  Project     = "data-processing"
  Terraform   = "true"
  Owner       = "YourName"
}
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Plan the Deployment

```bash
terraform plan -out=tfplan
```

### 5. Apply the Configuration

```bash
terraform apply tfplan
```

### 6. Testing the Deployment

After successful deployment, you'll see the API Gateway endpoint URL in the outputs.

Example API request:

```bash
# Set your API endpoint from terraform output
API_ENDPOINT=$(terraform output -raw api_endpoint)

# Make a request with the Bearer token
curl -X POST $API_ENDPOINT/data \
  -H "Authorization: Bearer valid-token" \
  -H "Content-Type: application/json" \
  -d '{"example": "data", "value": 123}'
```

## Cleanup

To destroy all resources created by Terraform:

```bash
terraform destroy
```

## Security Considerations

- The Lambda authorizer is configured to authenticate API requests
- All IAM roles follow the principle of least privilege
- S3 bucket has server-side encryption enabled
- DynamoDB table has encryption enabled

## Cost Considerations

This architecture uses serverless resources that scale based on usage:
- API Gateway: Pay per request and data transfer
- Lambda: Pay for execution time and requests
- Firehose: Pay for data ingestion and processing
- S3: Pay for storage and requests
- DynamoDB: Pay for storage and read/write capacity
- AWS Glue: Pay for catalog usage

For a development environment with moderate usage, the cost should be minimal.
