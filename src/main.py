import json
import os
import shutil
import numpy as np
from PIL import Image

import onnxmanager
from inference import first_slice, other_slices
from jsonmanager import json_manager
from onnxmanager import lists_builder, model_extractor, model_refactorer
from src.utils import cleaner
from src.s3manager import s3_local_manager
from src import constants

if __name__ == '__main__':

    # Do not forget to delete all files from previous executions
    cleaner.purge_all_except_pattern(onnxmanager.JSON_ROOT_PATH, "README.md")
    cleaner.purge_all_except_pattern(onnxmanager.EVENTS_PATH, "README.md")

    inputs, outputs = lists_builder.build_lists()

    cleaner.purge(onnxmanager.SLICES_PATH, "")
    model_extractor.extract_model_slices(inputs, outputs)

    outputs = model_refactorer.refactor_slices(inputs, outputs)

    slice_index = 0
    json_manager.make_event(slice_index, inputs, outputs)
    shutil.copy(json_manager.get_event_path(0), "../../onnx-decomposer_aws/events/event0.json")
    print("event0.json created successfully")

    # MOBILEDET:
    img = np.load(onnxmanager.INPUT_IMAGE_PATH)
    img = img.astype("float32")
    first_slice.run(img, slice_index, inputs, outputs)

    for slice_index in range(1, constants.NUMBER_OF_SLICES):
        other_slices.run(slice_index, inputs, outputs)

    result = json_manager.get_payload_content("TFLite_Detection_PostProcess")
    print("\nRESULTS:")
    print(result[0][0])
    # END MOBILEDET

    # EFFICIENTDET:
    # images = []
    # for f in [onnxmanager.INPUT_IMAGE_PATH]:
    #     images.append(np.array(Image.open(f)))
    # img = np.array(images, dtype='uint8')
    # first_slice.run(img, slice_index, inputs, outputs)
    #
    # for slice_index in range(1, constants.NUMBER_OF_SLICES):
    #     other_slices.run(slice_index, inputs, outputs)
    #
    # result = json_manager.get_payload_content("detections:0")
    # print("\nRESULTS:")
    # print(result[0][0])
    # END EFFICIENTDET

    # UPLOAD ONNX FILES TO S3
    # COMMENT THIS IF NOT USED !!!
    s3_local_manager.upload_onnx_slices()
    # END UPLOAD ONNX FILES TO S3
