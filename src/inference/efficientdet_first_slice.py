import numpy as np
import onnxruntime
import PIL
from PIL import Image

from src import constants
from src import inference
from src.onnxmanager import model_extractor
from src.jsonmanager import json_manager


def get_results():
    images = []
    for f in [inference.INPUT_IMAGE_PATH]:
        images.append(np.array(PIL.Image.open(f)))

    img = np.array(images, dtype='uint8')
    model_slice0_path = model_extractor.get_slice_path(0)

    session = onnxruntime.InferenceSession(model_slice0_path)
    results = session.run(None, {constants.INPUT_LIST_START[0]: img})

    return results


def run(slice_index, input_lists, output_lists):
    results = get_results()

    for i in range(len(results)):
        result = results[i]
        json_manager.payload_to_jsonfile(output_lists[0][i], result)

    # LOCAL ONLY
    next_payload_index = json_manager.get_next_payload_index()
    json_manager.make_event(slice_index + 1, next_payload_index, input_lists, output_lists)
    # END LOCAL ONLY

    print("Slice 0: execution completed successfully")

