import os
import pathlib
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
import tf2onnx

import preliminaries_constants as plm_constants


tensorflow_model_path = pathlib.Path(plm_constants.TENSORFLOW_MODEL_PATH)

if not os.path.exists(tensorflow_model_path):
    tensorflow_model_path.mkdir(parents=True)

model = ResNet50(weights='imagenet')
model.save(tensorflow_model_path)

spec = (tf.TensorSpec((None, 224, 224, 3), tf.float32, name="input"),)

model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec, opset=13, output_path=plm_constants.ONNX_MODEL_PATH)
