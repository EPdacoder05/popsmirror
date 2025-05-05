from flask import Flask, render_template, jsonify, request
import subprocess
import boto3

app = Flask(__name__)

# Compliance Check Functions
def check_ebs_encryption():
    ec2 = boto3.client('ec2')
    vols = ec2.describe_volumes()
    unencrypted = [v['VolumeId'] for v in vols['Volumes'] if not v['Encrypted']]
    if unencrypted:
        return {"status": "FAIL", "unencrypted_volumes": unencrypted}
    return {"status": "PASS", "unencrypted_volumes": []}

def check_s3_encryption():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()["Buckets"]
    unencrypted_buckets = []
    for bucket in buckets:
        try:
            enc = s3.get_bucket_encryption(Bucket=bucket["Name"])
            rules = enc["ServerSideEncryptionConfiguration"]["Rules"]
            if not any(r["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"] == "aws:kms" for r in rules):
                unencrypted_buckets.append(bucket["Name"])
        except Exception:
            unencrypted_buckets.append(bucket["Name"])
    if unencrypted_buckets:
        return {"status": "FAIL", "unencrypted_buckets": unencrypted_buckets}
    return {"status": "PASS", "unencrypted_buckets": []}

# Locust Performance Test
def run_locust_test():
    try:
        # Run Locust in headless mode
        result = subprocess.run(
            ["locust", "-f", "locustfile.py", "--headless", "-u", "100", "-r", "10", "-t", "1m"],
            capture_output=True,
            text=True,
        )
        return {"status": "SUCCESS", "output": result.stdout}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@app.route("/")
def home():
    return render_template("index.html")

# Security Engineers: Endpoint for EBS compliance check
@app.route("/check_ebs", methods=["GET"])
def check_ebs():
    result = check_ebs_encryption()
    return jsonify(result)

# Security Engineers: Endpoint for S3 compliance check
@app.route("/check_s3", methods=["GET"])
def check_s3():
    result = check_s3_encryption()
    return jsonify(result)

# App Developers & Data Engineers: Endpoint to run Locust performance tests
@app.route("/run_locust", methods=["POST"])
def run_locust():
    result = run_locust_test()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)