import shutil

import onnxmanager
from inference import first_slice, other_slices
from jsonmanager import json_manager
from onnxmanager import lists_builder, model_extractor, model_refactorer
from src.utils import cleaner
from src.utils import sizes_helper, payload_size_calculator, package_size_calculator
from src.s3manager import s3_local_manager
from src import constants

import importlib
project_steps = importlib.import_module(constants.PROJECT_STEPS_MODULE, package=None)

if __name__ == '__main__':

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

    img = project_steps.get_preprocessed_input()
    first_slice.run(img, slice_index, inputs, outputs)

    for slice_index in range(1, constants.NUMBER_OF_SLICES):
        other_slices.run(slice_index, inputs, outputs)

    result = project_steps.get_result()
    print("\nRESULTS:")
    print(result)

    # UPLOAD ONNX FILES TO S3
    # COMMENT THIS IF NOT USED !!!
    # s3_local_manager.upload_onnx_slices()
    # END UPLOAD ONNX FILES TO S3

    # PAYLOADS SIZES
    print("\nVIRTUAL PAYLOADS SIZES PER SLICE:")
    payloads_sizes = payload_size_calculator.get_payloads_sizes()
    # print(payloads_sizes)

    pretty_payloads_sizes = sizes_helper.get_pretty_sizes(payloads_sizes)
    print(pretty_payloads_sizes)

    # PACKAGES SIZES
    # print("\nPACKAGES SIZES:")
    # packages_sizes = package_size_calculator.get_packages_sizes()
    # print(packages_sizes)
    #
    # pretty_packages_sizes = sizes_helper.get_pretty_sizes(packages_sizes)
    # print(pretty_packages_sizes)
