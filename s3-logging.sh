#!/bin/bash
loggingBucket='s3-logging-sydney-default' 
region='ap-southeast-2'

# Create Logging bucket 

aws s3 mb s3://$loggingBucket --region $region 
echo bucket $loggingBucket created in region $region
aws s3api put-bucket-acl --bucket $loggingBucket --grant-write URI=http://acs.amazonaws.com/groups/s3/LogDelivery --grant-read-acp URI=http://acs.amazonaws.com/groups/s3/LogDelivery
echo ACL configured for bucket $loggingBucket

#setting logging for each bucket in this region

for b in $(aws s3api --output text list-buckets --query "Buckets[].Name"); do
  if [ $(aws s3api --output text get-bucket-location --bucket $b) == $region ]; then
    if [ $b != $loggingBucket ]; then
      echo updating logging configuration for $b in region $region
      aws s3api put-bucket-logging --bucket $b --bucket-logging-status "{\"LoggingEnabled\": {\"TargetBucket\": \"$loggingBucket\",\"TargetPrefix\": \"$b/\"}}"
    fi
  fi
done
