import os

from src import onnxmanager
from src.utils import size_helper


def get_slice_sizes():
    slice_sizes = []
    slice_filenames = os.listdir(onnxmanager.SLICES_PATH)

    for i in range(len(slice_filenames)):
        slice_path = onnxmanager.SLICES_PATH + slice_filenames[i]
        slice_sizes += [os.path.getsize(slice_path)]
    return slice_sizes


def get_maximum_slice_size():
    slice_sizes = get_slice_sizes()
    max_slice_size = max(slice_sizes)
    max_slice_index = slice_sizes.index(max_slice_size)
    return max_slice_size, max_slice_index


def print_max_slice_size():
    max_slice_size, max_slice_index = get_maximum_slice_size()
    pretty_max_slice_size = size_helper.get_pretty_size(max_slice_size)
    print("MAXIMUM SLICE SIZE:")
    print(pretty_max_slice_size + " (" + str(max_slice_size) + " bytes) (Slice " + str(max_slice_index) + ")")
