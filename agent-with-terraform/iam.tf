# IAM Role for Lambda functions
resource "aws_iam_role" "lambda_role" {
  name = "${local.name_prefix}-lambda-role-${local.resource_suffix}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

# IAM Policy for Lambda basic execution
resource "aws_iam_policy" "lambda_basic" {
  name        = "${local.name_prefix}-lambda-basic-policy-${local.resource_suffix}"
  description = "Basic execution policy for Lambda functions"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# IAM Policy for Lambda to access Firehose
resource "aws_iam_policy" "lambda_firehose" {
  name        = "${local.name_prefix}-lambda-firehose-policy-${local.resource_suffix}"
  description = "Policy for Lambda to put records to Firehose"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "firehose:PutRecord",
          "firehose:PutRecordBatch"
        ]
        Effect   = "Allow"
        Resource = aws_kinesis_firehose_delivery_stream.main.arn
      }
    ]
  })
}

# IAM Policy for Lambda to access DynamoDB
resource "aws_iam_policy" "lambda_dynamodb" {
  name        = "${local.name_prefix}-lambda-dynamodb-policy-${local.resource_suffix}"
  description = "Policy for Lambda to access DynamoDB"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem"
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.main.arn
      }
    ]
  })
}

# Attach policies to Lambda IAM role
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_basic.arn
}

resource "aws_iam_role_policy_attachment" "lambda_firehose" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_firehose.arn
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_dynamodb.arn
}

# IAM Role for Firehose
resource "aws_iam_role" "firehose_role" {
  name = "${local.name_prefix}-firehose-role-${local.resource_suffix}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "firehose.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

# IAM Policy for Firehose to access S3
resource "aws_iam_policy" "firehose_s3" {
  name        = "${local.name_prefix}-firehose-s3-policy-${local.resource_suffix}"
  description = "Policy for Firehose to put objects in S3"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:AbortMultipartUpload",
          "s3:GetBucketLocation",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:ListBucketMultipartUploads",
          "s3:PutObject"
        ]
        Effect   = "Allow"
        Resource = [
          aws_s3_bucket.firehose_bucket.arn,
          "${aws_s3_bucket.firehose_bucket.arn}/*"
        ]
      }
    ]
  })
}

# IAM Policy for Firehose to invoke Lambda
resource "aws_iam_policy" "firehose_lambda" {
  name        = "${local.name_prefix}-firehose-lambda-policy-${local.resource_suffix}"
  description = "Policy for Firehose to invoke Lambda"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "lambda:InvokeFunction",
          "lambda:GetFunctionConfiguration"
        ]
        Effect   = "Allow"
        Resource = aws_lambda_function.consumer.arn
      }
    ]
  })
}

# IAM Policy for Firehose to access Glue
resource "aws_iam_policy" "firehose_glue" {
  name        = "${local.name_prefix}-firehose-glue-policy-${local.resource_suffix}"
  description = "Policy for Firehose to access Glue"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "glue:GetTable",
          "glue:GetTableVersion",
          "glue:GetTableVersions"
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:catalog",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:database/${aws_glue_catalog_database.main.name}",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:table/${aws_glue_catalog_database.main.name}/${aws_glue_catalog_table.main.name}"
        ]
      }
    ]
  })
}

# Attach policies to Firehose IAM role
resource "aws_iam_role_policy_attachment" "firehose_s3" {
  role       = aws_iam_role.firehose_role.name
  policy_arn = aws_iam_policy.firehose_s3.arn
}

resource "aws_iam_role_policy_attachment" "firehose_lambda" {
  role       = aws_iam_role.firehose_role.name
  policy_arn = aws_iam_policy.firehose_lambda.arn
}

resource "aws_iam_role_policy_attachment" "firehose_glue" {
  role       = aws_iam_role.firehose_role.name
  policy_arn = aws_iam_policy.firehose_glue.arn
}

# Get current AWS account ID
data "aws_caller_identity" "current" {}
