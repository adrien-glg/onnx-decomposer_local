import os
import onnx

from src import constants
from src import onnxmanager


def get_slice_path(slice_index):
    """
    Returns the path of the specified ONNX slice.
    :param slice_index: Index of the slice for which we want to know the path.
    :return:
    """
    directory = onnxmanager.SLICES_PATH
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory + constants.PROJECT_NAME + "_slice" + str(slice_index).zfill(2) + ".onnx"


def get_slice_path_s3(slice_index):
    """
    Returns the path of the specified ONNX slice, for AWS S3.
    :param slice_index: Index of the slice for which we want to know the path, for AWS S3.
    :return:
    """
    directory = onnxmanager.SLICES_PATH_S3
    return directory + constants.PROJECT_NAME + "_slice" + str(slice_index).zfill(2) + ".onnx"


def extract_slice(model_slice_path, input_list, output_list):
    """
    Extracts a slice from the original ONNX model, and saves it to the model_slice_path.
    :param model_slice_path: Path to which the slice will be saved.
    :param input_list: List of the inputs of the slice we want to extract.
    :param output_list: List of the outputs of the slice we want to extract.
    """
    onnx.utils.extract_model(onnxmanager.MODEL_PATH, model_slice_path, input_list, output_list)


def extract_model_slices(input_lists, output_lists):
    """
    Extracts as many slices as there are elements in input_lists (equal to the number of elements in output_lists),
    from the original ONNX model.
    :param input_lists: List of the inputs of each slice we want to extract.
    :param output_lists: List of the outputs of each slice we want to extract.
    """
    for slice_index in range(constants.NUMBER_OF_SLICES):
        model_slice_path = get_slice_path(slice_index)
        extract_slice(model_slice_path, input_lists[slice_index], output_lists[slice_index])
        print("Slice " + str(slice_index) + " extracted successfully")
