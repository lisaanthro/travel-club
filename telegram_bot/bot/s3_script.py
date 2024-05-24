import boto3

from config_reader import config

S3_BUCKET_NAME = "travel-club"

session = boto3.session.Session()
s3_client = session.client(
    service_name="s3",
    aws_access_key_id=config.AWS_ACCESS_KEY_ID.get_secret_value(),
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY.get_secret_value(),
    endpoint_url=config.ENDPOINT_URL.get_secret_value(),
)


def get_all_buckets(s3: boto3.session.Session.client):
    response = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in response.get("Buckets")]
    return buckets


def create_bucket(s3: boto3.session.Session.client, bucket_name: str):
    s3.create_bucket(Bucket=bucket_name)


if __name__ == "__main__":
    print(get_all_buckets(s3_client))
