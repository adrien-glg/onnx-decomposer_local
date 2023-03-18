from configparser import ConfigParser

config_parser = ConfigParser()
config_parser.read('../../general_config.ini')

PROJECT_NAME = config_parser.get('project', 'project_name')

MODEL_PATH = "../../models/" + PROJECT_NAME + "/"
TENSORFLOW_MODEL_PATH = MODEL_PATH + PROJECT_NAME + "_tensorflow"
ONNX_MODEL_PATH = MODEL_PATH + PROJECT_NAME + ".onnx"

config_parser.read(PROJECT_NAME + "_config.ini")

INPUT = config_parser.get('input', 'input')

INPUT_PATH = MODEL_PATH + INPUT
