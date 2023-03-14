import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np

import preliminaries_constants as plm_constants


img = image.load_img(plm_constants.INPUT_PATH, target_size=(224, 224))

x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

output_path = os.path.splitext(plm_constants.INPUT_PATH)[0]
np.save(output_path, img)
