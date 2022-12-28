import os

from src.jsonmanager import json_manager
from src import onnxmanager


def get_s3_payloads_paths():
    paths = json_manager.get_payloads_paths()
    final_payloads_paths = []
    for path in paths:
        final_payloads_paths += [onnxmanager.JSON_ROOT_PATH_S3 + "/" + os.path.basename(path)]
    return final_payloads_paths


def get_s3_dictionary_path():
    s3_path = onnxmanager.JSON_ROOT_PATH_S3 + "/" + os.path.basename(onnxmanager.DICTIONARY_PATH)
    return s3_path
