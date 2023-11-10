import boto3
import botocore

bucketlist = [
]

client = boto3.client("s3")
buckets = bucketlist["Buckets"]

for bucket in buckets:
    try:
        client.get_bucket_encryption(Bucket=bucket["Name"])
    # If we catch a ServerSideEncryptionConfigurationNotFoundError, the bucket doesn't have
    # default encryption at rest enabled. Confirm with the user and enable it.
    
    except botocore.exceptions.ClientError as error:
        if (
            error.response["Error"]["Code"]
            == "ServerSideEncryptionConfigurationNotFoundError"
        ):
            confirmation = input(
                f'Enable at-rest encryption by default for {bucket["Name"]}? [Y/n]: '
            )
            if confirmation.upper() == "Y" or confirmation == "":
                client.put_bucket_encryption(
                    Bucket=bucket["Name"],
                    ServerSideEncryptionConfiguration={
                        "Rules": [
                            {
                                "ApplyServerSideEncryptionByDefault": {
                                    "SSEAlgorithm": "AES256"
                                }
                            },
                        ]
                    },
                )
        elif (
            error.response["Error"]["Code"]
            == "AccessDenied" or "IllegalLocationConstraintException"
        ):
            print("Access on bucket:" ,bucket["Name"], "is denied, skipping this bucket")            
            continue 
        else:
            raise error
