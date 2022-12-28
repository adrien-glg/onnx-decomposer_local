import json
import os

from src import onnxmanager

next_payload_index = 0
dict_init_completed = False
payloads_paths = []


def get_next_payload_index():
    return next_payload_index


def set_next_payload_index(new_next_payload_index):
    global next_payload_index
    next_payload_index = new_next_payload_index


def get_payloads_paths():
    return payloads_paths


def init_dictionary():
    global dict_init_completed
    if not os.path.exists(onnxmanager.JSON_ROOT_PATH):
        os.mkdir(onnxmanager.JSON_ROOT_PATH)
    init_data = json.dumps({})
    with open(onnxmanager.DICTIONARY_PATH, 'w') as outfile:
        outfile.write(init_data)
        outfile.close()
    dict_init_completed = True


# key: output name
# value: filepath
def update_dictionary(key, value):
    with open(onnxmanager.DICTIONARY_PATH) as file:
        file_data = json.load(file)
        file_data[key] = value

    with open(onnxmanager.DICTIONARY_PATH, 'w') as file:
        json.dump(file_data, file, indent=4)


def get_new_filepath():
    global next_payload_index
    global payloads_paths
    new_filepath = os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[0] + str(next_payload_index) + \
        os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[1]
    next_payload_index += 1
    payloads_paths += [new_filepath]
    return new_filepath


def payload_to_jsonfile(key, data):
    global dict_init_completed
    if not dict_init_completed:
        init_dictionary()

    data = data.tolist()
    data = json.dumps(data)

    filepath = get_new_filepath()
    json_file = open(filepath, "w")
    json_file.write(data)
    json_file.close()

    update_dictionary(key, filepath)


def get_payload_content(key):
    with open(onnxmanager.DICTIONARY_PATH) as dictionary:
        dict_data = json.load(dictionary)
        payload_path = dict_data[key]

    with open(payload_path, "r") as jsonfile:
        payload_content = json.load(jsonfile)

    return payload_content


def get_event_path(slice_index):
    if not os.path.exists(onnxmanager.JSON_ROOT_PATH):
        os.mkdir(onnxmanager.JSON_ROOT_PATH)
    event_path = os.path.splitext(onnxmanager.EVENT_PATH)[0] + str(slice_index) + \
        os.path.splitext(onnxmanager.EVENT_PATH)[1]
    return event_path


def make_event(slice_index, next_payload_index, input_lists, output_lists):
    event = {"next_slice_index": slice_index, "next_payload_index": next_payload_index, "inputs": input_lists, "outputs": output_lists}
    json_event = json.dumps(event, indent=4)
    filepath = get_event_path(slice_index)
    json_file = open(filepath, "w")
    json_file.write(json_event)
    json_file.close()
