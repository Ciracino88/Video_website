import boto3
from dotenv import load_dotenv
import os

class s3_class():
    def __init__(self):
        load_dotenv()
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region_name = os.getenv('REGION_NAME')

        session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name
        )
        self.inst = session.client('s3')
