import json
import os

from src import onnxmanager

FILES_COUNTER = 0
DICT_INIT_COMPLETED = False


def init_dictionary():
    global DICT_INIT_COMPLETED
    os.mkdir(onnxmanager.JSON_ROOT_PATH)
    init_data = json.dumps({})
    with open(onnxmanager.DICTIONARY_PATH, 'w') as outfile:
        outfile.write(init_data)
        outfile.close()
    DICT_INIT_COMPLETED = True


# key: output name
# value: filepath
def update_dictionary(key, value):
    with open(onnxmanager.DICTIONARY_PATH) as file:
        file_data = json.load(file)
        file_data[key] = value

    with open(onnxmanager.DICTIONARY_PATH, 'w') as file:
        json.dump(file_data, file, indent=4)


def get_new_filepath():
    global FILES_COUNTER
    new_filepath = os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[0] + str(FILES_COUNTER) + os.path.splitext(onnxmanager.JSON_PAYLOAD_PATH)[1]
    FILES_COUNTER += 1
    return new_filepath


def payload_to_jsonfile(key, data):
    global DICT_INIT_COMPLETED
    if not DICT_INIT_COMPLETED:
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
