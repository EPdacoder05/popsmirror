# Parameterize placeholder values 
variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"  # Change as needed
}

variable "aws_profile" {
  description = "AWS CLI profile to use"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  description = "AZ for resources"
  type        = string
  default     = "us-east-1a"
}

variable "trusted_ips" {
  description = "List of trusted IP CIDR blocks"
  type        = list(string)
}

variable "ami_id" {
  description = "Hardened AMI ID for EC2 instance"
  type        = string
}

variable "bucket_name" {
  description = "Name for S3 bucket"
  type        = string
}