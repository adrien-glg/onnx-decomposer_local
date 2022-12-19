import boto3

from src import onnxmanager
from src.jsonmanager import json_manager
from src.inference import mobiledet_first_slice, other_slices

S3_BUCKET = "onnx-mobiledet-bucket"
PAYLOAD_INDEX = 0

s3 = boto3.client('s3')


def lambda_handler(event, context):
    slice_index = event['next_slice_index']
    payload_index = event['next_payload_index']
    inputs = event['inputs']
    outputs = event['outputs']

    if slice_index == 0:
        mobiledet_first_slice.run(outputs)
    else:
        other_slices.run(slice_index, payload_index, inputs, outputs)

    dictionary_path = onnxmanager.DICTIONARY_PATH
    s3.upload_file(dictionary_path, S3_BUCKET)

    payloads_paths = json_manager.get_payloads_paths()
    for filepath in payloads_paths:
        s3.upload_file(filepath, S3_BUCKET)

    next_slice_index = slice_index + 1
    next_payload_index = json_manager.get_next_payload_index()

    output_event = {"next_slice_index": next_slice_index, "next_payload_index": next_payload_index,
                    "inputs": inputs, "outputs": outputs}

    return {
        'statusCode': 200,
        'body': output_event
    }
