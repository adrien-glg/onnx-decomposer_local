import onnxruntime

from src import constants
from src.onnxmanager import model_extractor
from src.jsonmanager import json_manager


def get_results(input_file):
    """
    Computes and returns the results of the first slice execution.
    :param input_file: Model input data, such as an image for image classification.
    :return: Computed results for the first slice.
    """
    model_slice0_path = model_extractor.get_slice_path(0)

    session = onnxruntime.InferenceSession(model_slice0_path)
    results = session.run(None, {constants.INPUT_LIST_START[0]: input_file})

    return results


def run(input_file, input_lists, output_lists):
    """
    Computes the results (payloads) of the first slice execution, and saves each of them in a separate JSON file.
    Makes the input event for the following slice execution.
    :param input_file: Model input data, such as an image for image classification.
    :param input_lists: List of the matching inputs for each slice.
    :param output_lists: List of the matching output for each slice.
    """
    slice_index = 0
    results = get_results(input_file)

    for i in range(len(results)):
        result = results[i]
        json_manager.payload_to_jsonfile(slice_index, output_lists[0][i], result)

    json_manager.set_next_payload_index(0)
    json_manager.make_event(slice_index + 1, input_lists, output_lists)  # only locally, not for AWS

    print("Slice 0: execution completed successfully")


def run(input_file):
    """
    Computes the results (payloads) of the first slice execution, and saves each of them in a separate JSON file.
    Makes the input event for the following slice execution.
    :param input_file: Model input data, such as an image for image classification.
    """
    slice_index = 0
    results = get_results(input_file)
    input_lists, output_lists = json_manager.get_inputs_outputs_from_event(slice_index)

    for i in range(len(results)):
        result = results[i]
        json_manager.payload_to_jsonfile(slice_index, output_lists[0][i], result)

    json_manager.set_next_payload_index(0)
    json_manager.make_event(slice_index + 1, input_lists, output_lists)  # only locally, not for AWS

    print("Completed slice 1 execution successfully")
