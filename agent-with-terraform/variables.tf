variable "aws_region" {
  description = "AWS region where resources will be deployed"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "data-processing"
}

variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "lambda_zip_path" {
  description = "Path to the zip file containing the main Lambda function code"
  type        = string
  default     = "lambda/main-function.zip"
}

variable "authorizer_zip_path" {
  description = "Path to the zip file containing the authorizer Lambda function code"
  type        = string
  default     = "lambda/authorizer-function.zip"
}

variable "consumer_zip_path" {
  description = "Path to the zip file containing the consumer Lambda function code"
  type        = string
  default     = "lambda/consumer-function.zip"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "dev"
    Project     = "data-processing"
    Terraform   = "true"
  }
}
