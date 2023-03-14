import numpy as np
from src import onnxmanager
from src.jsonmanager import json_manager


def get_preprocessed_input():
    input_array = np.load(onnxmanager.INPUT_IMAGE_PATH)
    input_float = input_array.astype("float32")
    final_input = np.array([input_float])
    return final_input


def get_result():
    result = json_manager.get_payload_content("predictions")
    result = result[0][0]
    return result
