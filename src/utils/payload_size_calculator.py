import os.path
import glob

from src import onnxmanager
from src import constants
from src.utils import size_helper


# PAYLOADS PER SLICE:
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


# PAYLOADS PER LAYER:
# def get_all_payload_sizes(outputs):
#     payload_sizes = []
#     outputs = outputs[0]
#
#     for payload_index in range(len(outputs)):
#         payload_path = os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[0] + "0_" + str(payload_index) + \
#                        os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[1]
#         payload_size = os.path.getsize(payload_path)
#         payload_sizes += [payload_size]
#
#     return payload_sizes
def get_all_payload_sizes():
    payload_sizes = []
    payload_filenames = os.listdir(onnxmanager.JSON_ROOT_PATH)
    payload_filenames.remove(os.path.basename(onnxmanager.DICTIONARY_PATH))
    payload_filenames.remove("README.md")

    for i in range(len(payload_filenames)):
        payload_path = onnxmanager.JSON_ROOT_PATH + payload_filenames[i]
        payload_sizes += [os.path.getsize(payload_path)]
    return payload_sizes


# PAYLOAD PER SLICE:
def print_payload_sizes():
    payload_sizes = get_payload_sizes()
    slice_indices = [i for i, x in sorted(enumerate(payload_sizes), key=lambda x: x[1])]
    slice_indices.reverse()
    payload_sizes.sort(reverse=True)
    pretty_payload_sizes = size_helper.get_pretty_sizes(payload_sizes)
    print("VIRTUAL PAYLOAD SIZE PER SLICE (SORTED):")
    for i in range(len(pretty_payload_sizes)):
        print("Slice " + str(slice_indices[i]) + ": " + pretty_payload_sizes[i])


# PAYLOAD PER LAYER:
def print_all_payload_sizes():
    payload_sizes = get_all_payload_sizes()
    slice_indices = [i for i, x in sorted(enumerate(payload_sizes), key=lambda x: x[1])]
    slice_indices.reverse()
    payload_sizes.sort(reverse=True)
    pretty_payload_sizes = size_helper.get_pretty_sizes(payload_sizes)
    print("\nPAYLOAD SIZE PER LAYER (SORTED):")
    for i in range(len(pretty_payload_sizes)):
        print("Layer " + str(slice_indices[i]) + ": " + pretty_payload_sizes[i])




