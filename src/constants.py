# MOBILEDET:
PROJECT_NAME = "mobiledet"
ONNX_MODEL = "mobiledet.onnx"
INPUT_IMAGE = "img_resized.npy"
INPUT_LIST_START = ['normalized_input_image_tensor']
OUTPUT_LIST_END = ["TFLite_Detection_PostProcess", "TFLite_Detection_PostProcess:1",
                   "TFLite_Detection_PostProcess:2", "TFLite_Detection_PostProcess:3"]
S3_BUCKET = "onnx-mobiledet-bucket"


# EFFICIENTDET
# PROJECT_NAME = "efficientdet"
# ONNX_MODEL = "efficientdet-d2.onnx"
# INPUT_IMAGE = "img_efficientdet.png"
# INPUT_LIST_START = ["image_arrays:0"]
# OUTPUT_LIST_END = ['detections:0']
# S3_BUCKET = "onnx-efficientdet-bucket"

NUMBER_OF_SLICES = 5


