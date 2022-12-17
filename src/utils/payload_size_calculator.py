import os.path

from src import onnxmanager


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


# f_size = os.path.getsize('../data/payload0.json')
# x = convert_bytes(f_size)
# print(x)
