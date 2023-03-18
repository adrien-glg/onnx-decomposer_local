import shutil

import onnxmanager
from inference import first_slice, other_slices
from jsonmanager import json_manager
from onnxmanager import lists_builder, model_extractor, model_refactorer
from src.utils import cleaner
from src.s3manager import s3_local_manager
from src import constants

import importlib
project_steps = importlib.import_module(constants.PROJECT_STEPS_MODULE, package=None)

if __name__ == '__main__':

    print("PROJECT: " + constants.PROJECT_NAME + ", " + str(constants.NUMBER_OF_SLICES) + " slices\n")
    cleaner.purge_all_except_pattern(onnxmanager.JSON_ROOT_PATH, "README.md")
    cleaner.purge_all_except_pattern(onnxmanager.EVENTS_PATH, "README.md")

    inputs, outputs = lists_builder.build_lists()

    cleaner.purge(onnxmanager.SLICES_PATH, "")
    model_extractor.extract_model_slices(inputs, outputs)

    outputs = model_refactorer.refactor_slices(inputs, outputs)

    slice_index = 0
    json_manager.make_event(slice_index, inputs, outputs)
    shutil.copy(json_manager.get_event_path(0), constants.EVENT_COPY_PATH)
    print("event0.json created successfully")

    img = project_steps.get_preprocessed_input()
    first_slice.run(img, slice_index, inputs, outputs)

    for slice_index in range(1, constants.NUMBER_OF_SLICES):
        other_slices.run(slice_index, inputs, outputs)

    result = project_steps.get_result()
    print("\nRESULTS:")
    print(result)

    # To save S3 costs, comment this if not used!
    s3_local_manager.upload_onnx_slices()
