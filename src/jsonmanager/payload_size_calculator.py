import os.path

from src import onnxmanager
from src.onnxmanager import model_extractor


# calculate file size in KB, MB, GB
def convert_bytes(size):
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, unit)
        size /= 1024.0


def get_payloads_sizes(outputs):
    payloads_sizes_per_slice = []
    payload_counter = 0

    for slice_index in range(len(outputs)):
        slice_payload_size = 0
        for payload_index in range(len(outputs[slice_index])):
            payload_path = os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[0] + str(payload_counter) + os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[1]
            payload_size = os.path.getsize(payload_path)
            slice_payload_size += payload_size
            payload_counter += 1
        payloads_sizes_per_slice += [slice_payload_size]

    return payloads_sizes_per_slice


def get_pretty_payloads_sizes(outputs):
    pretty_payloads_sizes = []
    payloads_sizes = get_payloads_sizes(outputs)

    for slice_index in range(len(payloads_sizes)):
        pretty_payloads_sizes += [convert_bytes(payloads_sizes[slice_index])]

    return pretty_payloads_sizes


# f_size = os.path.getsize('../data/payload0.json')
# x = convert_bytes(f_size)
# print(x)
