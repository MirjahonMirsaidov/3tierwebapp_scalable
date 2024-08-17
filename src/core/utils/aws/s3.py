import uuid

import boto3
s3_resource = boto3.resource('s3')


class S3:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    @staticmethod
    def generate_file_url(file_name):
        random_file_name = '_'.join([str(uuid.uuid4().hex[:6]), file_name])
        return random_file_name

    def upload_file(self, file_name, obj):
        file_name = self.generate_file_url(file_name)
        s3_resource.Bucket(self.bucket_name).Object(file_name).put(Body=obj)
        return file_name

    def download_file(self, file_name, object_name):
        s3_resource.Bucket(self.bucket_name).download_file(file_name, object_name)

    def delete_file(self, object_name):
        s3_resource.Object(self.bucket_name, object_name).delete()

    def get_file(self, object_name):
        return s3_resource.Object(self.bucket_name, object_name).get()

    def list_files(self):
        return s3_resource.Bucket(self.bucket_name).objects.all()

    def list_buckets(self):
        return s3_resource.buckets.all()


cdn_client = S3(bucket_name='mirjahon-aws-s3')
