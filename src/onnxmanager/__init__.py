import os
import onnx

from src import constants

MODEL_PATH = "../models/" + constants.PROJECT_NAME + "/" + constants.ONNX_MODEL
JSON_ROOT_PATH = "data"
JSON_PAYLOAD_PATH = "data/payload.json"
DICTIONARY_PATH = "data/filenames_dictionary.json"
SLICES_PATH = "../models/" + constants.PROJECT_NAME + "/slices"

