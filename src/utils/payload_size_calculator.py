import os.path
import glob

from src import onnxmanager
from src import constants
from src.utils import size_helper


# FUNCTION TO BE USED WITH MAIN_ALL_PAYLOADS.PY ONLY
def get_all_payload_sizes(outputs):
    payload_sizes = []
    outputs = outputs[0]

    for payload_index in range(len(outputs)):
        payload_path = os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[0] + "0_" + str(payload_index) + \
                       os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[1]
        payload_size = os.path.getsize(payload_path)
        payload_sizes += [payload_size]

    return payload_sizes


def get_payload_sizes():
    payload_sizes_per_slice = []

    for slice_index in range(constants.NUMBER_OF_SLICES):
        slice_payload_size = 0
        payload_path_pattern = os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[0] + str(slice_index) + "*.json"
        slice_payloads = glob.glob(payload_path_pattern)
        for i in range(len(slice_payloads)):
            payload_size = os.path.getsize(slice_payloads[i])
            slice_payload_size += payload_size
        payload_sizes_per_slice += [slice_payload_size]

    return payload_sizes_per_slice


def print_payload_sizes():
    payload_sizes = get_payload_sizes()
    pretty_payload_sizes = size_helper.get_pretty_sizes(payload_sizes)
    print("VIRTUAL PAYLOAD SIZES PER SLICE:")
    for i in range(len(pretty_payload_sizes)):
        print("Slice " + str(i) + ": " + pretty_payload_sizes[i])
