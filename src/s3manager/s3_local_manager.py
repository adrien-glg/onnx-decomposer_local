import boto3

from src import onnxmanager
from src import constants
from src.onnxmanager import model_extractor

s3 = boto3.client('s3')


def get_buckets_list():
    """
    Returns the list of your AWS S3 buckets.
    :return: List of buckets.
    """
    buckets = s3.list_buckets()['Buckets']
    buckets_list = []
    for i in range(len(buckets)):
        buckets_list += [buckets[i]['Name']]
    return buckets_list


def create_bucket():
    """
    Creates the AWS S3 bucket specified in the project configuration file, if it does not already exist.
    """
    buckets_list = get_buckets_list()
    bucket = constants.S3_BUCKET
    if bucket not in buckets_list:
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': constants.AWS_REGION})


def delete_onnx_slices():
    """
    Deletes all the ONNX slices from the AWS S3 bucket.
    """
    try:
        objects = s3.list_objects(Bucket=constants.S3_BUCKET, Prefix=onnxmanager.SLICES_PATH_S3)['Contents']
    except KeyError:
        objects = []
    if len(objects) > 0:
        delete_keys = {'Objects': [{'Key': obj['Key']} for obj in objects]}
        s3.delete_objects(Bucket=constants.S3_BUCKET, Delete=delete_keys)


def upload_onnx_slices():
    """
    Uploads the ONNX slices from the immediate past execution to the AWS S3 bucket.
    """
    print("Uploading slices to S3...")
    create_bucket()
    delete_onnx_slices()
    for slice_index in range(constants.NUMBER_OF_SLICES):
        model_slice_path = model_extractor.get_slice_path(slice_index)
        model_slice_path_s3 = model_extractor.get_slice_path_s3(slice_index)
        s3.upload_file(model_slice_path, constants.S3_BUCKET, model_slice_path_s3)
    print("Uploaded slices successfully\n")
