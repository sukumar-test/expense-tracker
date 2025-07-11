terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}

# Random ID for unique resource naming
resource "random_id" "suffix" {
  byte_length = 4
}

# Define locals for naming conventions
locals {
  name_prefix = "${var.project_name}-${var.environment}"
  resource_suffix = random_id.suffix.hex
}

# API Gateway
resource "aws_apigatewayv2_api" "main" {
  name          = "${local.name_prefix}-api-${local.resource_suffix}"
  protocol_type = "HTTP"
  description   = "API Gateway for the ${var.project_name} application"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE"]
    allow_headers = ["Content-Type", "Authorization"]
    max_age       = 300
  }

  tags = var.tags
}

# API Gateway stage
resource "aws_apigatewayv2_stage" "main" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = var.environment
  auto_deploy = true

  default_route_settings {
    throttling_burst_limit = 100
    throttling_rate_limit  = 50
  }

  tags = var.tags
}

# Main Lambda Function
resource "aws_lambda_function" "main" {
  function_name = "${local.name_prefix}-lambda-${local.resource_suffix}"
  description   = "Main Lambda function for the ${var.project_name} application"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs18.x"
  timeout       = 30
  memory_size   = 256

  filename         = var.lambda_zip_path
  source_code_hash = filebase64sha256(var.lambda_zip_path)

  environment {
    variables = {
      ENVIRONMENT  = var.environment
      FIREHOSE_DELIVERY_STREAM = aws_kinesis_firehose_delivery_stream.main.name
    }
  }

  tags = var.tags
}

# Authorizer Lambda Function
resource "aws_lambda_function" "authorizer" {
  function_name = "${local.name_prefix}-authorizer-${local.resource_suffix}"
  description   = "Authorizer Lambda function for the ${var.project_name} application"
  role          = aws_iam_role.lambda_role.arn
  handler       = "authorizer.handler"
  runtime       = "nodejs18.x"
  timeout       = 10
  memory_size   = 128

  filename         = var.authorizer_zip_path
  source_code_hash = filebase64sha256(var.authorizer_zip_path)

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }

  tags = var.tags
}

# Consumer Lambda Function
resource "aws_lambda_function" "consumer" {
  function_name = "${local.name_prefix}-consumer-${local.resource_suffix}"
  description   = "Consumer Lambda function for the ${var.project_name} application"
  role          = aws_iam_role.lambda_role.arn
  handler       = "consumer.handler"
  runtime       = "nodejs18.x"
  timeout       = 30
  memory_size   = 256

  filename         = var.consumer_zip_path
  source_code_hash = filebase64sha256(var.consumer_zip_path)

  environment {
    variables = {
      ENVIRONMENT = var.environment
      DYNAMODB_TABLE = aws_dynamodb_table.main.name
    }
  }

  tags = var.tags
}

# Lambda authorizer for API Gateway
resource "aws_apigatewayv2_authorizer" "main" {
  api_id           = aws_apigatewayv2_api.main.id
  authorizer_type  = "REQUEST"
  identity_sources = ["$request.header.Authorization"]
  name             = "lambda-authorizer"
  authorizer_uri   = aws_lambda_function.authorizer.invoke_arn

  authorizer_payload_format_version = "2.0"
  enable_simple_responses          = true
}

# API Gateway integration with Lambda
resource "aws_apigatewayv2_integration" "main" {
  api_id                 = aws_apigatewayv2_api.main.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.main.invoke_arn
  payload_format_version = "2.0"
  timeout_milliseconds   = 30000
}

# API Gateway default route
resource "aws_apigatewayv2_route" "main" {
  api_id             = aws_apigatewayv2_api.main.id
  route_key          = "ANY /{proxy+}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.main.id
  target             = "integrations/${aws_apigatewayv2_integration.main.id}"
}

# Lambda permission for API Gateway
resource "aws_lambda_permission" "api_gateway_main" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*/{proxy+}"
}

# Lambda permission for API Gateway to invoke Authorizer
resource "aws_lambda_permission" "api_gateway_authorizer" {
  statement_id  = "AllowAPIGatewayInvokeAuthorizer"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.authorizer.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/authorizers/${aws_apigatewayv2_authorizer.main.id}"
}

# S3 bucket for Firehose data
resource "aws_s3_bucket" "firehose_bucket" {
  bucket = "${local.name_prefix}-firehose-${local.resource_suffix}"

  tags = var.tags
}

# Enable S3 bucket versioning
resource "aws_s3_bucket_versioning" "firehose_bucket_versioning" {
  bucket = aws_s3_bucket.firehose_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Server-side encryption for S3 bucket
resource "aws_s3_bucket_server_side_encryption_configuration" "firehose_bucket_encryption" {
  bucket = aws_s3_bucket.firehose_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Firehose Delivery Stream
resource "aws_kinesis_firehose_delivery_stream" "main" {
  name        = "${local.name_prefix}-delivery-stream-${local.resource_suffix}"
  destination = "extended_s3"

  extended_s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.firehose_bucket.arn
    
    prefix              = "data/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/"
    error_output_prefix = "errors/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/!{firehose:error-output-type}/"
    
    buffer_size        = 64
    buffer_interval    = 60
    compression_format = "PARQUET"
    
    data_format_conversion_configuration {
      input_format_configuration {
        deserializer {
          hive_json_ser_de {}
        }
      }
      
      output_format_configuration {
        serializer {
          parquet_ser_de {}
        }
      }
      
      schema_configuration {
        database_name = aws_glue_catalog_database.main.name
        table_name    = aws_glue_catalog_table.main.name
        role_arn      = aws_iam_role.firehose_role.arn
      }
    }

    processing_configuration {
      enabled = true

      processors {
        type = "Lambda"

        parameters {
          parameter_name  = "LambdaArn"
          parameter_value = aws_lambda_function.consumer.arn
        }
      }
    }
  }

  tags = var.tags
}

# Trigger consumer Lambda from Firehose
resource "aws_lambda_permission" "firehose_consumer" {
  statement_id  = "AllowFirehoseInvokeConsumer"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.consumer.function_name
  principal     = "firehose.amazonaws.com"
  source_arn    = aws_kinesis_firehose_delivery_stream.main.arn
}

# DynamoDB table
resource "aws_dynamodb_table" "main" {
  name         = "${local.name_prefix}-table-${local.resource_suffix}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }

  tags = var.tags
}

# AWS Glue Database
resource "aws_glue_catalog_database" "main" {
  name        = "${replace(local.name_prefix, "-", "_")}_database_${local.resource_suffix}"
  description = "Database for ${var.project_name} data"
}

# AWS Glue Table
resource "aws_glue_catalog_table" "main" {
  name          = "${replace(local.name_prefix, "-", "_")}_table"
  database_name = aws_glue_catalog_database.main.name
  
  table_type = "EXTERNAL_TABLE"
  
  parameters = {
    "classification"      = "parquet"
    "compressionType"     = "none"
    "typeOfData"          = "file"
    "EXTERNAL"            = "TRUE"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.firehose_bucket.bucket}/data/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
    
    ser_de_info {
      name                  = "ParquetHiveSerDe"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
      
      parameters = {
        "serialization.format" = 1
      }
    }

    # Define your schema based on your data structure
    columns {
      name = "id"
      type = "string"
    }
    
    columns {
      name = "timestamp"
      type = "timestamp"
    }
    
    columns {
      name = "data"
      type = "string"
    }

    # Add more columns as needed
  }
}

# CloudWatch Log Groups for Lambda functions
resource "aws_cloudwatch_log_group" "main_lambda" {
  name              = "/aws/lambda/${aws_lambda_function.main.function_name}"
  retention_in_days = 14
  tags              = var.tags
}

resource "aws_cloudwatch_log_group" "authorizer_lambda" {
  name              = "/aws/lambda/${aws_lambda_function.authorizer.function_name}"
  retention_in_days = 14
  tags              = var.tags
}

resource "aws_cloudwatch_log_group" "consumer_lambda" {
  name              = "/aws/lambda/${aws_lambda_function.consumer.function_name}"
  retention_in_days = 14
  tags              = var.tags
}

# Output values
output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = "${aws_apigatewayv2_stage.main.invoke_url}"
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.main.name
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.firehose_bucket.bucket
}

output "firehose_delivery_stream_name" {
  description = "Name of the Firehose delivery stream"
  value       = aws_kinesis_firehose_delivery_stream.main.name
}

output "glue_database_name" {
  description = "Name of the Glue catalog database"
  value       = aws_glue_catalog_database.main.name
}

output "glue_table_name" {
  description = "Name of the Glue catalog table"
  value       = aws_glue_catalog_table.main.name
}
