import boto3

from src import constants
from src.onnxmanager import model_extractor

s3 = boto3.client('s3')


def get_buckets_list():
    buckets = s3.list_buckets()['Buckets']
    buckets_list = []
    for i in range(len(buckets)):
        buckets_list += [buckets[i]['Name']]
    return buckets_list


def create_bucket():
    buckets_list = get_buckets_list()
    bucket = constants.S3_BUCKET
    if bucket not in buckets_list:
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': constants.AWS_REGION})


def upload_onnx_slices():
    create_bucket()
    for slice_index in range(constants.NUMBER_OF_SLICES):
        model_slice_path = model_extractor.get_slice_path(slice_index)
        model_slice_path_s3 = model_extractor.get_slice_path_s3(slice_index)
        s3.upload_file(model_slice_path, constants.S3_BUCKET, model_slice_path_s3)
