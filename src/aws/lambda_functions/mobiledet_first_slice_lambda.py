import numpy as np
import onnxruntime

from src import constants
from src import inference
from src.onnxmanager import model_extractor
from src.jsonmanager import json_manager


def get_results():
    img = np.load(inference.INPUT_IMAGE_PATH)
    model_slice0_path = model_extractor.get_slice_path(0)

    session = onnxruntime.InferenceSession(model_slice0_path)
    results = session.run(None, {constants.INPUT_LIST_START[0]: img.astype("float32")})

    return results


def run(output_lists):
    results = get_results()
    for i in range(len(results)):
        result = results[i]
        json_manager.payload_to_jsonfile(output_lists[0][i], result)
