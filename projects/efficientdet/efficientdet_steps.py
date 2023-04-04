import numpy as np
from src import onnxmanager
from src.jsonmanager import json_manager
from PIL import Image


def get_preprocessed_input():
    images = []
    for f in [onnxmanager.INPUT_IMAGE_PATH]:
        images.append(np.array(Image.open(f)))
    img = np.array(images, dtype='uint8')
    return img


def get_result():
    result = json_manager.get_payload_data("detections:0")
    result = result[0][0]
    return result
