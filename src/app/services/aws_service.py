import boto3

from config import settings


class AWSService:
    def __init__(self):
        self.region_name = settings.AWS_REGION_NAME
        self.bucket_name = settings.AWS_BUCKET

    def import_s3_files(self, path: str):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=self.region_name,
        )

        response = s3_client.list_objects_v2(Bucket=self.bucket_name)
        # Verificar si se obtuvieron objetos
        if "Contents" in response:
            # Obtener la lista de objetos y sus nombres
            objects = response["Contents"]
            for obj in objects:
                local_file = path + obj["Key"]
                s3_client.download_file(self.bucket_name, obj["Key"], local_file)

    def run_notify_lambda(self):
        lambda_client = boto3.client(
            "lambda",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=self.region_name,
        )

        function_name = "notify_lambda"
        lambda_client.invoke(
            FunctionName=function_name,
        )
