import os
import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME


class CloudManager:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

    def upload_file(self, file_path):
        try:
            file_name = os.path.basename(file_path)
            self.s3.upload_file(file_path, BUCKET_NAME, file_name)
            print("Uploaded to cloud successfully.")
            return True
        except Exception as e:
            print("Upload failed:", e)
            return False

    def upload_and_delete(self, file_path):
        success = self.upload_file(file_path)

        if success:
            os.remove(file_path)
            print("Local file deleted.")
        else:
            print("File kept on PC.")