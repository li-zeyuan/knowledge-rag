from minio import Minio
from application.settings import MINIO
from datetime import timedelta
import uuid

endpoint = f"{MINIO['HOST']}:{MINIO['PORT']}"

client = Minio(endpoint,MINIO['ACCESS_KEY'],MINIO['SECRET_KEY'], secure=False)

if not client.bucket_exists(MINIO['BUCKET']):
    client.make_bucket(MINIO['BUCKET'])

def gen_presigned_put_url(file_name):
    file_suffix = file_name.split('.')[-1]
    hash_key = uuid.uuid1()
    key = f"{hash_key}.{file_suffix}"
    url = client.presigned_put_object(MINIO['BUCKET'], key, expires=timedelta(minutes=2))

    return url, key

def download_file(key, file_path):
    client.fget_object(MINIO['BUCKET'], key, file_path)