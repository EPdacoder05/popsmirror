provider "aws" {
  region  = "#YOUR_AWS_REGION" 
  profile = "#YOUR_AWS_PROFILE" 
}

resource "aws_kms_key" "prod_encryption" {
  description         = "POPSMirror Encryption Key"  # KMS key for encrypting resources (compliance)
  enable_key_rotation = true # Rotates encryption key automatically for security
}

resource "aws_kms_key" "ebs" {
  description         = "EBS encryption key for POPSMirror" # Dedicated KMS key for EBS volumes
  enable_key_rotation = true
  tags = {
    Name = "POPSMirror-EBS-KMS"
  }
}

resource "aws_vpc" "main" {
  cidr_block           = "#YOUR_VPC_CIDR"
  enable_dns_hostnames = true # Allows EC2 instances to resolve DNS names
  tags = { Name = "POPSMirror-VPC" }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id #Attach subnet to the VPC above
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "main" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "#YOUR_SUBNET_CIDR"
  availability_zone = "#YOUR_AZ"
  tags = { Name = "POPSMirror-Subnet" }
}

resource "aws_network_acl" "private" {
  vpc_id = aws_vpc.main.id
  subnet_ids = [aws_subnet.private.id]

  egress {
    protocol   = "-1"
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  ingress {
    protocol   = "tcp"
    rule_no    = 100
    action     = "allow"
    cidr_block = var.trusted_ip
    from_port  = 443
    to_port    = 443
  }
}

resource "aws_security_group" "main" {
  name        = "POPSMirror-SG"
  vpc_id      = aws_vpc.main.id
  description = "Restrict to trusted IPs"
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["#TRUSTED_IPS"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app" {
  ami                    = "#HARDENED_AMI_ID" # Use a secure, patched AMI (e.g., CIS-hardened)
  instance_type          = "t3.medium"
  subnet_id              = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.main.id]

  root_block_device {
    encrypted  = true # Encrypt the root disk for compliance
    kms_key_id = aws_kms_key.ebs.arn # Use your dedicated KMS key
  }

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required" # Enforce IMDSv2 for instance metadata (prevents SSRF)
  }

  tags = { Name = "POPSMirror-App" }
}

resource "aws_config_configuration_recorder" "main" {
  name     = "prodmirror-compliance"
  role_arn = aws_iam_role.config.arn # Role for AWS Config to record resource changes
}

resource "aws_cloudtrail" "audit" {
  name                          = "prodmirror-audit"
  s3_bucket_name                = aws_s3_bucket.logs.id # Store audit logs in S3 for compliance
  include_global_service_events = true # Capture all AWS service events
  enable_logging                = true # Turn on logging for CloudTrail
}

resource "aws_s3_bucket" "test_data" {
  bucket = "#YOUR_BUCKET_NAME"
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm     = "aws:kms" # Enforce KMS encryption for all objects
        kms_master_key_id = aws_kms_key.ebs.arn
      }
    }
  }
  tags = { Name = "POPSMirror-Test-Data" }
}
