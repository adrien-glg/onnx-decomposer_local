from inference import first_slice, other_slices
from jsonmanager import json_manager
from onnxmanager import lists_builder, model_extractor, model_adjuster
from src.utils import cleaner, result_printer
from src.s3manager import s3_local_manager
from src import constants

import importlib
project_steps = importlib.import_module(constants.PROJECT_STEPS_MODULE, package=None)

if __name__ == '__main__':

    # Delete the remaining files from previous executions
    cleaner.purge()

    # Decompose the ONNX model in multiple slices
    inputs, outputs = lists_builder.get_built_lists()
    model_extractor.extract_model_slices(inputs, outputs)
    outputs = model_adjuster.adjust_slices(inputs, outputs)

    # Create the first event (only to prepare a future execution with AWS)
    json_manager.make_and_export_event(0, inputs, outputs)

    # Load the input data
    img = project_steps.get_preprocessed_input()

    # Run the inference
    first_slice.run(img, inputs, outputs)
    for slice_index in range(1, constants.NUMBER_OF_SLICES):
        other_slices.run(slice_index, inputs, outputs)

    # Print the results
    result_printer.print_result()

    # Upload the ONNX slices to AWS S3 for future AWS executions
    s3_local_manager.upload_onnx_slices()  # if not used: comment this line to save S3 costs
