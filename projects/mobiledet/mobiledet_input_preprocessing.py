import numpy as np
import cv2
import os

from projects import preliminaries_constants as plm_constants


def normalize(image):
    img = np.asarray(image, dtype='float32')
    img /= 255.0
    img -= 0.5
    img *= 2
    return img


def cv2_processing(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (320, 320), interpolation=cv2.INTER_LINEAR)
    img = normalize(img)
    img = np.expand_dims(img, axis=0)
    return img


img_path = plm_constants.INPUT_PATH
preprocessed_img = cv2_processing(img_path)
output_name = os.path.splitext(img_path)[0] + "_preprocessed"
np.save(output_name, preprocessed_img)
