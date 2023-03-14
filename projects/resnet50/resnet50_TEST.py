import onnxruntime as rt
import numpy as np
from tensorflow.keras.applications.resnet50 import decode_predictions

import preliminaries_constants as plm_constants

input_array = np.load(plm_constants.INPUT_PATH)
input_float = input_array.astype("float32")
final_input = np.array([input_float])

output_names = ['predictions']

m = rt.InferenceSession(plm_constants.ONNX_MODEL_PATH)
onnx_prediction = m.run(output_names, {"input": final_input})

print('ONNX Predicted:', onnx_prediction[0][0][0])
print('ONNX Predicted:', decode_predictions(onnx_prediction[0], top=3)[0])
