import numpy as np
import onnxruntime

from src import constants
from src import inference
from src.onnxmanager import model_extractor
from src.jsonmanager import json_manager



def get_results(input_file):
    model_slice0_path = model_extractor.get_slice_path(0)

    session = onnxruntime.InferenceSession(model_slice0_path)
    results = session.run(None, {constants.INPUT_LIST_START[0]: input_file})

    return results


def run(input_file, slice_index, input_lists, output_lists):
    results = get_results(input_file)

    for i in range(len(results)):
        result = results[i]
        json_manager.payload_to_jsonfile(slice_index, output_lists[0][i], result)

    json_manager.set_next_payload_index(0)
    # LOCAL ONLY
    json_manager.make_event(slice_index + 1, input_lists, output_lists)
    # END LOCAL ONLY

    print("Slice 0: execution completed successfully")
