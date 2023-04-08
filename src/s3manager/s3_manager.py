import boto3

import os
import pathlib

from src import constants
from src.jsonmanager import json_manager
from src.onnxmanager import model_extractor
from src import onnxmanager

s3 = boto3.client('s3')


def init_dictionary_on_s3():
    """
    Initializes the filenames dictionary by creating an empty JSON file on AWS S3.
    """
    json_manager.init_dictionary()
    s3.upload_file(onnxmanager.DICTIONARY_PATH, constants.S3_BUCKET, onnxmanager.DICTIONARY_PATH_S3)


def upload_dictionary_to_s3():
    """
    Uploads the filenames dictionary JSON file to AWS S3.
    """
    s3.upload_file(onnxmanager.DICTIONARY_PATH, constants.S3_BUCKET, onnxmanager.DICTIONARY_PATH_S3)


def download_dictionary():
    """
    Downloads the filenames dictionary JSON file from AWS S3.
    """
    s3.download_file(constants.S3_BUCKET, onnxmanager.DICTIONARY_PATH_S3, onnxmanager.DICTIONARY_PATH)


def delete_dictionary():
    """
    Deletes the filenames dictionary JSON file from AWS S3.
    """
    s3.delete_object(Bucket=constants.S3_BUCKET, Key=onnxmanager.DICTIONARY_PATH_S3)


def get_s3_payload_paths():
    """
    Returns a list of the payload paths in AWS S3.
    :return: List of the payload paths in AWS S3.
    """
    paths = json_manager.get_payloads_paths()
    final_payloads_paths = []
    for path in paths:
        p = pathlib.Path(path)
        final_payloads_paths += [str(p.relative_to(*p.parts[:2]))]
    return final_payloads_paths


def upload_payloads_to_s3():
    """
    Uploads all the payloads to AWS S3.
    """
    payloads_paths = json_manager.get_payloads_paths()
    payloads_paths_s3 = get_s3_payload_paths()
    for i in range(len(payloads_paths)):
        s3.upload_file(payloads_paths[i], constants.S3_BUCKET, payloads_paths_s3[i])
    json_manager.reset_payloads_paths()


def download_payload(filepath):
    """
    Downloads the payload relative to the specified filepath from AWS S3.
    :param filepath: Filepath of the payload we want to download.
    """
    if not os.path.exists(onnxmanager.JSON_ROOT_PATH):
        os.mkdir(onnxmanager.JSON_ROOT_PATH)
    s3_filepath = json_manager.remove_tmp_from_path(filepath)
    s3.download_file(constants.S3_BUCKET, s3_filepath, filepath)


def delete_payloads_from_s3():
    """
    Delete all payloads from AWS S3.
    """
    PREFIX = os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH_S3)[0]
    response = s3.list_objects_v2(Bucket=constants.S3_BUCKET, Prefix=PREFIX)

    if 'Contents' in response.keys():
        for file in response['Contents']:
            s3.delete_object(Bucket=constants.S3_BUCKET, Key=file['Key'])


def download_onnx_slice(slice_index):
    """
    Downloads the ONNX slice relative to the specified slice index from AWS S3.
    :param slice_index: Index of the slice we want to download.
    """
    slice_path = model_extractor.get_slice_path(slice_index)
    slice_path_s3 = model_extractor.get_slice_path_s3(slice_index)
    s3.download_file(constants.S3_BUCKET, slice_path_s3, slice_path)
