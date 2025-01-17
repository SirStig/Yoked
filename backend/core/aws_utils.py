import boto3
from botocore.exceptions import NoCredentialsError
from backend.core.config import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)

def upload_file_to_s3(file, filename):
    try:
        s3_client.upload_fileobj(
            file.file,
            settings.S3_BUCKET_NAME,
            filename,
            ExtraArgs={"ContentType": file.content_type}
        )
        return f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
    except NoCredentialsError:
        raise Exception("AWS credentials not found")
