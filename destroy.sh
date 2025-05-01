#!/bin/bash
terraform destroy -auto-approve
aws kms schedule-key-deletion --key-id $(aws kms list-keys --query 'Keys[0].KeyId' --output text) --pending-window-in-days 7