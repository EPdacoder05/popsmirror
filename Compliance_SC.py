import boto3 # 7: AWS SDK for Python to interact with cloud resources

def check_ebs_encryption(): # 6: Function to check if all EBS volumes are encrypted
    ec2 = boto3.client('ec2') # 5: Connect to EC2 service
    vols = ec2.describe_volumes() # 4: Get all EBS volumes in the account
    unencrypted = [v['VolumeId'] for v in vols['Volumes'] if not v['Encrypted']] # 3: List any unencrypted volumes
    if unencrypted:
        print(f"FAIL: Unencrypted EBS volumes: {unencrypted}") # 2: Print and fail if any are unencrypted
        exit(1)
    print("PASS: All EBS volumes encrypted.") # 1: Success message if all are encrypted

if __name__ == "__main__":
    check_ebs_encryption() # 0: Run the check when script is executed
