import os.path
import glob

from src import onnxmanager
from src import constants


# FUNCTION TO BE USED WITH MAIN_ALL_PAYLOADS.PY ONLY
def get_all_payloads_sizes(outputs):
    payloads_sizes = []
    outputs = outputs[0]

    for payload_index in range(len(outputs)):
        payload_path = os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[0] + "0_" + str(payload_index) + \
                       os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[1]
        payload_size = os.path.getsize(payload_path)
        payloads_sizes += [payload_size]

    return payloads_sizes


def get_payloads_sizes():
    payloads_sizes_per_slice = []

    for slice_index in range(constants.NUMBER_OF_SLICES):
        slice_payload_size = 0
        payload_path_pattern = os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[0] + str(slice_index) + "*.json"
        slice_payloads = glob.glob(payload_path_pattern)
        for i in range(len(slice_payloads)):
            payload_size = os.path.getsize(slice_payloads[i])
            slice_payload_size += payload_size
        payloads_sizes_per_slice += [slice_payload_size]

    return payloads_sizes_per_slice
