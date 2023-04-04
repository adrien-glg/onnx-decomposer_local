import json
import os
import pathlib

from src import onnxmanager
from src import constants

next_payload_index = 0
dict_init_completed = False
payloads_paths = []


def get_next_payload_index():
    """
    Returns the index of the next payload.
    :return:
    """
    return next_payload_index


def set_next_payload_index(payload_index):
    """
    Sets the index of the next payload.
    :param payload_index: Index of the next payload we want to set.
    :return:
    """
    global next_payload_index
    next_payload_index = payload_index


def get_payloads_paths():
    """
    Returns payloads paths.
    :return:
    """
    return payloads_paths


def reset_payloads_paths():
    """
    Resets the payloads paths to an empty list.
    """
    global payloads_paths
    payloads_paths = []


def get_new_filepath(slice_index):
    """
    Returns the filepath of the ONNX slice corresponding to the specified slice index.
    :param slice_index: Index of the slice we want to know the path.
    :return:
    """
    global next_payload_index
    global payloads_paths
    new_filepath = os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[0] + str(slice_index) + "_" + \
        str(next_payload_index) + os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[1]
    next_payload_index += 1
    payloads_paths += [new_filepath]
    return new_filepath


def remove_tmp_from_path(path):
    """
    Returns a new path in which "/tmp" at the start of the specified path has been removed.
    :param path: Path for which we want to remove "/tmp".
    :return: Filepath with "/tmp" removed.
    """
    filepath = pathlib.Path(path)
    new_filepath = str(filepath.relative_to(*filepath.parts[:2]))
    return new_filepath


def init_dictionary():
    """
    Initializes the filenames dictionary by creating an empty JSON file.
    """
    global dict_init_completed
    if not os.path.exists(onnxmanager.JSON_ROOT_PATH):
        os.mkdir(onnxmanager.JSON_ROOT_PATH)
    init_data = json.dumps({})
    with open(onnxmanager.DICTIONARY_PATH, 'w') as outfile:
        outfile.write(init_data)
        outfile.close()
    dict_init_completed = True


def update_dictionary(key, value):
    """
    Updates the filenames dictionaries by adding the specified key and value.
    :param key: Layer output name.
    :param value: Filepath in which the payload data will be stored.
    """
    with open(onnxmanager.DICTIONARY_PATH) as file:
        file_data = json.load(file)
        file_data[key] = value  # only locally, not for AWS

    with open(onnxmanager.DICTIONARY_PATH, 'w') as file:
        json.dump(file_data, file, indent=4)


def payload_to_jsonfile(slice_index, key, data):
    """
    Stores payload data in a JSON file.
    :param slice_index: Index of the slice to which the payload corresponds.
    :param key: Layer output name.
    :param data: Payload data to store in the JSON file.
    """
    global dict_init_completed
    if not dict_init_completed:
        init_dictionary()

    data = data.tolist()
    data = json.dumps(data)

    filepath = get_new_filepath(slice_index)
    json_file = open(filepath, "w")
    json_file.write(data)
    json_file.close()

    update_dictionary(key, filepath)


def get_payload_data(key):
    """
    Returns the payload data corresponding to the specified output.
    :param key: Layer output name for which we want the payload data.
    :return: Payload data.
    """
    with open(onnxmanager.DICTIONARY_PATH) as dictionary:
        dict_data = json.load(dictionary)
        payload_path = dict_data[key]

    with open(payload_path, "r") as jsonfile:
        payload_data = json.load(jsonfile)

    return payload_data


def get_event_path(slice_index):
    """
    Returns the path of the event corresponding to the specified slice.
    :param slice_index: Index of the slice for which we want the event path.
    :return: Event path.
    """
    if not os.path.exists(onnxmanager.JSON_ROOT_PATH):
        os.mkdir(onnxmanager.JSON_ROOT_PATH)
    event_path = os.path.splitext(onnxmanager.EVENT_PATH)[0] + str(slice_index) + \
        os.path.splitext(onnxmanager.EVENT_PATH)[1]
    return event_path


def make_event(slice_index, input_lists, output_lists):
    """
    Creates an event and stores it in a JSON file.
    :param slice_index: Index of the slice.
    :param input_lists: List of the matching inputs for each slice.
    :param output_lists: List of the matching output for each slice.
    """
    number_of_slices = constants.NUMBER_OF_SLICES
    keep_going = slice_index < number_of_slices
    event = {"keep_going": keep_going, "number_of_slices": number_of_slices, "next_slice_index": slice_index,
             "inputs": input_lists, "outputs": output_lists}
    json_event = json.dumps(event, indent=4)
    filepath = get_event_path(slice_index)
    json_file = open(filepath, "w")
    json_file.write(json_event)
    json_file.close()
