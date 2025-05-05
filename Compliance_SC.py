import boto3 # AWS SDK for Python to interact with cloud resources

def check_ebs_encryption(): # Function to check if all EBS volumes are encrypted
    ec2 = boto3.client('ec2') # Connect to EC2 service
    vols = ec2.describe_volumes() # Get all EBS volumes in the account
    unencrypted = [v['VolumeId'] for v in vols['Volumes'] if not v['Encrypted']] # List any unencrypted volumes
    if unencrypted:
        print(f"FAIL: Unencrypted EBS volumes: {unencrypted}") # Print and fail if any are unencrypted
        exit(1)
    print("PASS: All EBS volumes encrypted.") # Success message if all are encrypted

if __name__ == "__main__":
    check_ebs_encryption()
