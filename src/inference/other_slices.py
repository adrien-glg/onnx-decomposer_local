import numpy as np
import onnxruntime

from src.onnxmanager import model_extractor
from src.jsonmanager import json_manager


def get_payload(input_key):
    """
    Returns the payload data related to the specified input key.
    :param input_key: Name of the input for which we want the payload data.
    :return: Payload data
    """
    payload = json_manager.get_payload_data(input_key)
    final_payload = np.asarray(payload, dtype=np.float32)

    return final_payload


def get_results(slice_index, input_lists):
    """
    Computes and returns the results of the execution with the specified slice.
    :param slice_index: Index of the slice for which we want to compute the results.
    :param input_lists: List of the matching inputs for each slice.
    :return: Computed results for the specified slice.
    """
    model_slice_path = model_extractor.get_slice_path(slice_index)
    input_feed = {}

    for input_index in range(len(input_lists[slice_index])):
        input_key = input_lists[slice_index][input_index]
        payload = get_payload(input_key)
        input_feed[input_key] = payload

    session = onnxruntime.InferenceSession(model_slice_path)
    results = session.run(None, input_feed)

    return results


def run(slice_index):
    """
    Computes the results (payloads) of the specified slice execution, and saves each of them in a separate JSON file.
    Makes the input event for the following slice execution.
    :param slice_index: Index of the slice for which we want to compute the results.
    """
    input_lists, output_lists = json_manager.get_inputs_outputs_from_event(slice_index)
    results = get_results(slice_index, input_lists)

    for i in range(len(results)):
        result = results[i]
        json_manager.payload_to_jsonfile(slice_index, output_lists[slice_index][i], result)

    json_manager.set_next_payload_index(0)
    json_manager.make_event(slice_index + 1, input_lists, output_lists)  # only locally, not for AWS

    print("Completed slice " + str(slice_index + 1) + " execution successfully")
