#!/bin/bash

# Set your AWS region
AWS_REGION="your_aws_region"

# Set your EC2 instance IDs separated by space
EC2_INSTANCE_IDS="instance_id_1 instance_id_2"

# Set your RDS instance IDs separated by space
RDS_DB_INSTANCE_IDS="db_instance_id_1 db_instance_id_2"

# Function to start EC2 instances
start_ec2() {
    aws ec2 start-instances --region $AWS_REGION --instance-ids $EC2_INSTANCE_IDS
    echo "EC2 instances started."
}

# Function to stop EC2 instances
stop_ec2() {
    aws ec2 stop-instances --region $AWS_REGION --instance-ids $EC2_INSTANCE_IDS
    echo "EC2 instances stopped."
}

# Function to start RDS instances
start_rds() {
    aws rds start-db-instance --region $AWS_REGION --db-instance-identifier $RDS_DB_INSTANCE_IDS
    echo "RDS instances started."
}

# Function to stop RDS instances
stop_rds() {
    aws rds stop-db-instance --region $AWS_REGION --db-instance-identifier $RDS_DB_INSTANCE_IDS
    echo "RDS instances stopped."
}

case "$1" in
    start)
        start_ec2
        start_rds
        ;;
    stop)
        stop_ec2
        stop_rds
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac

exit 0
