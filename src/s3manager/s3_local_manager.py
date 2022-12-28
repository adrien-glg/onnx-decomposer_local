import boto3

from src import constants
from src.onnxmanager import model_extractor

s3 = boto3.client('s3')


def upload_onnx_slices():
    for slice_index in range(constants.NUMBER_OF_SLICES):
        model_slice_path = model_extractor.get_slice_path(slice_index)
        model_slice_path_s3 = model_extractor.get_slice_path_s3(slice_index)
        s3.upload_file(model_slice_path, constants.S3_BUCKET, model_slice_path_s3)

