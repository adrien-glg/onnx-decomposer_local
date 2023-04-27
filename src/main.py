import os
import sys

from inference import first_slice, other_slices
from jsonmanager import json_manager
from src import onnxmanager
from onnxmanager import lists_builder, model_extractor, model_adjuster
from src.utils import cleaner, result_printer
from src.s3manager import s3_local_manager
from src.utils import size_helper, payload_size_calculator, max_slice_size_checker
from src import constants

import importlib

project_steps = importlib.import_module(constants.PROJECT_STEPS_MODULE, package=None)


def run():
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
    # s3_local_manager.upload_onnx_slices()  # if not used: comment this line to save S3 costs


def max_slice_size_mode():
    if not os.listdir(onnxmanager.SLICES_PATH):
        print("First, you need to run an execution with the 'exec' mode")
    max_slice_size_checker.print_max_slice_size()


def payloads_mode():
    if not os.listdir(onnxmanager.JSON_ROOT_PATH):
        print("First, you need to run an execution with the 'exec' mode")
    payload_size_calculator.print_payload_sizes()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = "exec"

    if mode == "exec":
        print("EXECUTION MODE\n")
        run()

    if mode == "max_slice_size":
        print("MAXIMUM SLICE SIZE MODE\n")
        max_slice_size_mode()

    if mode == "payloads":
        print("PAYLOADS MODE\n")
        payloads_mode()

