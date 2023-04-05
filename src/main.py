from inference import first_slice, other_slices
from jsonmanager import json_manager
from onnxmanager import lists_builder, model_extractor, model_adjuster
from src.utils import cleaner, result_printer
from src.s3manager import s3_local_manager
from src import constants

import importlib
project_steps = importlib.import_module(constants.PROJECT_STEPS_MODULE, package=None)

if __name__ == '__main__':

    cleaner.purge()

    inputs, outputs = lists_builder.get_built_lists()
    model_extractor.extract_model_slices(inputs, outputs)
    outputs = model_adjuster.adjust_slices(inputs, outputs)

    json_manager.make_and_export_event(0, inputs, outputs)

    img = project_steps.get_preprocessed_input()

    first_slice.run(img, inputs, outputs)
    for slice_index in range(1, constants.NUMBER_OF_SLICES):
        other_slices.run(slice_index, inputs, outputs)

    result_printer.print_result()

    # To save S3 costs: comment this if not used!
    s3_local_manager.upload_onnx_slices()
