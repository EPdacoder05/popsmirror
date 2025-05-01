# POPSMirror - Secure Performance Testing Environment

## Overview
POPSMirror creates a secure, compliant testing environment that mirrors production for healthcare applications. It enables safe performance testing while maintaining HIPAA compliance and security controls.

## Requirements
- AWS CLI with MFA configured
- Terraform >= 1.0
- Python 3.9+
- Locust >= 2.0
- Git

## Quick Setup
1. **Clone and configure:**
```bash
# Clone repository
git clone https://github.com/EPdacoder05/popsmirror.git
cd popsmirror

# Copy and edit configuration
cp terraform.tfvars.example terraform.tfvars
```

2. **Configure your environment:**
Edit `terraform.tfvars` with your specific values:
```hcl
aws_region = "us-east-1"
aws_profile = "your-profile"
vpc_cidr = "10.0.0.0/16"
subnet_cidr = "10.0.1.0/24"
availability_zone = "us-east-1a"
trusted_ips = ["10.0.0.0/8"]
ami_id = "ami-XXXXX"
bucket_name = "your-unique-bucket-name"
```

3. **Deploy infrastructure:**
```bash
terraform init
terraform apply
```

## Security Controls
- **Encryption**: All resources encrypted using KMS
- **Network**: Access restricted to trusted IPs via Security Groups and NACLs
- **Audit**: CloudTrail enabled for comprehensive logging
- **Compliance**: Automated checks via AWS Config
- **Data Protection**: S3 bucket encryption and versioning enabled

## Required Variables
| Name | Description | Example |
|------|-------------|---------|
| aws_region | AWS region for deployment | us-east-1 |
| aws_profile | AWS CLI profile name | healthcare-dev |
| vpc_cidr | VPC CIDR range | 10.0.0.0/16 |
| subnet_cidr | Subnet CIDR range | 10.0.1.0/24 |
| availability_zone | AWS AZ | us-east-1a |
| trusted_ips | List of allowed IP ranges | ["10.0.0.0/8"] |
| ami_id | Hardened AMI ID | ami-12345678 |
| bucket_name | Unique S3 bucket name | my-secure-test-bucket |

## Testing
```bash
# Run compliance checks
python compliance.py

# Run load tests
locust -f locustfile.py --headless -u 500 -r 50
```

## Cleanup
```bash
terraform destroy -auto-approve
```
