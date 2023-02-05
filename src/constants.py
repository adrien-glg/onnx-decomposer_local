from configparser import ConfigParser

config_parser = ConfigParser()
config_parser.read('../projectname_config.ini')

PROJECT_NAME = config_parser.get('project', 'project_name')

config_parser.read('../projects/' + PROJECT_NAME + "/" + PROJECT_NAME + "_config.ini")

ONNX_MODEL = config_parser.get('project', 'onnx_model')
INPUT_IMAGE = config_parser.get('project', 'input_image')
S3_BUCKET = config_parser.get('aws', 's3_bucket')
NUMBER_OF_SLICES = config_parser.getint('number_of_slices', 'number_of_slices')

parsed_input_list = config_parser.get('project', 'input_list_start')
INPUT_LIST_START = list(parsed_input_list.split("\n"))[1:]

parsed_output_list = config_parser.get('project', 'output_list_end')
OUTPUT_LIST_END = list(parsed_output_list.split("\n"))[1:]

PROJECT_STEPS_MODULE = "projects." + PROJECT_NAME + "." + PROJECT_NAME + "_steps"
