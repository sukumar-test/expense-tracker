aws_region   = "us-east-1"
project_name = "data-processing"
environment  = "dev"

# Lambda function paths
lambda_zip_path     = "lambda/dist/main-function.zip"
authorizer_zip_path = "lambda/dist/authorizer-function.zip"
consumer_zip_path   = "lambda/dist/consumer-function.zip"

tags = {
  Environment = "dev"
  Project     = "data-processing"
  Terraform   = "true"
  Owner       = "DevOps"
}
