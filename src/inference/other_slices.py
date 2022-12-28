import numpy as np
import onnxruntime

from src.onnxmanager import model_extractor
from src.jsonmanager import json_manager


def get_payload(input_key):
    payload = json_manager.get_payload_content(input_key)
    final_payload = np.asarray(payload, dtype=np.float32)

    return final_payload


def get_results(slice_index, input_lists):
    model_slice_path = model_extractor.get_slice_path(slice_index)
    input_feed = {}

    for input_index in range(len(input_lists[slice_index])):
        input_key = input_lists[slice_index][input_index]
        payload = get_payload(input_key)
        input_feed[input_key] = payload

    session = onnxruntime.InferenceSession(model_slice_path)
    results = session.run(None, input_feed)

    return results


def run(slice_index, next_payload_index, input_lists, output_lists):
    results = get_results(slice_index, input_lists)

    json_manager.set_next_payload_index(next_payload_index)

    for i in range(len(results)):
        result = results[i]
        json_manager.payload_to_jsonfile(output_lists[slice_index][i], result)

    # LOCAL ONLY
    next_payload_index = json_manager.get_next_payload_index()
    json_manager.make_event(slice_index + 1, next_payload_index, input_lists, output_lists)
    # END LOCAL ONLY

    print("Slice " + str(slice_index) + ": execution completed successfully")
