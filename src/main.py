import json
import os
import shutil

import onnxmanager
from inference import other_slices, mobiledet_first_slice, efficientdet_first_slice
from jsonmanager import json_manager
from onnxmanager import lists_builder, model_extractor, model_refactorer
from src.utils import sizes_helper, payload_size_calculator, package_size_calculator, cleaner
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

    slice_index, payload_index = 0, 0
    json_manager.make_event(slice_index, payload_index, inputs, outputs)
    shutil.copy(json_manager.get_event_path(0), "../../onnx-decomposer_aws/events/event0.json")
    print("event0.json created successfully")

    # MOBILEDET:
    mobiledet_first_slice.run(slice_index, inputs, outputs)

    for slice_index in range(1, constants.NUMBER_OF_SLICES):
        event_path = json_manager.get_event_path(slice_index)
        event = json.load(open(event_path))
        next_payload_index = event['next_payload_index']
        other_slices.run(slice_index, next_payload_index, inputs, outputs)

    result = json_manager.get_payload_content("TFLite_Detection_PostProcess")
    print("\nRESULTS:")
    print(result[0][0])
    # END MOBILEDET

    # EFFICIENTDET:
    # efficientdet_first_slice.run(slice_index, inputs, outputs)
    #
    # for slice_index in range(1, constants.NUMBER_OF_SLICES):
    #     event_path = json_manager.get_event_path(slice_index)
    #     event = json.load(open(event_path))
    #     next_payload_index = event['next_payload_index']
    #     other_slices.run(slice_index, next_payload_index, inputs, outputs)
    #
    # result = json_manager.get_payload_content("detections:0")
    # print("\nRESULTS:")
    # print(result[0][0])
    # END EFFICIENTDET

    # UPLOAD ONNX FILES TO S3
    # COMMENT THIS IF NOT USED !!!
    # s3_local_manager.upload_onnx_slices()
    # END UPLOAD ONNX FILES TO S3
