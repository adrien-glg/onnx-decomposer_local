import json
import os
import shutil

import onnxmanager
from inference import other_slices, mobiledet_first_slice, efficientdet_first_slice
from jsonmanager import json_manager
from onnxmanager import lists_builder, model_extractor, model_refactorer
from src.utils import sizes_helper, payload_size_calculator, package_size_calculator
from src.s3manager import s3_local_manager
from src import constants

if __name__ == '__main__':

    # Do not forget to delete all files from previous executions
    if os.path.exists(onnxmanager.JSON_ROOT_PATH):
        shutil.rmtree(onnxmanager.JSON_ROOT_PATH)

    inputs, outputs = lists_builder.build_lists()

    if os.path.exists(onnxmanager.SLICES_PATH):
        shutil.rmtree(onnxmanager.SLICES_PATH)
    model_extractor.extract_model_slices(inputs, outputs)

    outputs = model_refactorer.refactor_slices(inputs, outputs)

    slice_index, payload_index = 0, 0
    json_manager.make_event(slice_index, payload_index, inputs, outputs)

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
    # efficientdet_first_slice.run(outputs)
    #
    # for slice_index in range(1, constants.NUMBER_OF_SLICES):
    #     print(slice_index)
    #     other_slices.run(slice_index, inputs, outputs)
    #
    # result = jsonmanager.get_payload_content("detections:0")
    # print("\nRESULTS:")
    # print(result[0][0])
    # END EFFICIENTDET

    # UPLOAD ONNX FILES TO S3
    s3_local_manager.upload_onnx_slices()
    # END UPLOAD ONNX FILES TO S3

    # PAYLOADS SIZES
    # print("\nVIRTUAL PAYLOADS SIZES PER SLICE:")
    # payloads_sizes = payload_size_calculator.get_payloads_sizes(outputs)
    # print(payloads_sizes)
    #
    # pretty_payloads_sizes = sizes_helper.get_pretty_sizes(payloads_sizes)
    # print(pretty_payloads_sizes)
    #
    # # PACKAGES SIZES
    # print("\nPACKAGES SIZES:")
    # packages_sizes = package_size_calculator.get_packages_sizes()
    # print(packages_sizes)
    #
    # pretty_packages_sizes = sizes_helper.get_pretty_sizes(packages_sizes)
    # print(pretty_packages_sizes)
