import shutil

import onnxmanager
from inference import first_slice, other_slices
from jsonmanager import json_manager
from onnxmanager import lists_builder, model_extractor, model_adjuster
from src.utils import cleaner
from src.utils import size_helper, payload_size_calculator
from src.s3manager import s3_local_manager
from src import constants

import importlib
project_steps = importlib.import_module(constants.PROJECT_STEPS_MODULE, package=None)

if __name__ == '__main__':

    cleaner.purge_all_except_pattern(onnxmanager.JSON_ROOT_PATH, "README.md")
    cleaner.purge_all_except_pattern(onnxmanager.EVENTS_PATH, "README.md")

    inputs, outputs = lists_builder.get_built_lists()

    cleaner.purge(onnxmanager.SLICES_PATH, "")
    model_extractor.extract_model_slices(inputs, outputs)

    outputs = model_adjuster.adjust_slices(inputs, outputs)

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

    # PAYLOAD SIZES
    payload_sizes = payload_size_calculator.get_payload_sizes()
    pretty_payload_sizes = size_helper.get_pretty_sizes(payload_sizes)

    print("\nVIRTUAL PAYLOAD SIZES PER SLICE:")
    print(pretty_payload_sizes)
    # print(payload_sizes)
