import os
import argparse
from memory_profiler import profile

from inference import first_slice, other_slices
from jsonmanager import json_manager
from src import onnxmanager
from onnxmanager import lists_builder, model_extractor, model_adjuster
from src.utils import cleaner, result_printer, payload_size_calculator, max_slice_size_checker, slice_checker
from src.s3manager import s3_local_manager
from src import constants

import importlib
project_steps = importlib.import_module(constants.PROJECT_STEPS_MODULE, package=None)


def run_decomposition(selected_mode):
    print("Starting decomposition:")

    # Delete the remaining files from previous executions
    cleaner.purge()

    # Decompose the ONNX model in multiple slices
    inputs, outputs = lists_builder.get_built_lists()
    if selected_mode == "payload_per_layer":
        outputs = lists_builder.get_all_outputs()
        model_adjuster.add_all_model_outputs(outputs)
    else:
        model_extractor.extract_model_slices(inputs, outputs)
        outputs = model_adjuster.adjust_slices(inputs, outputs)

    # Create the first event (only to prepare a future execution with AWS)
    json_manager.make_and_export_event(0, inputs, outputs)

    # Upload the ONNX slices to AWS S3 for future AWS executions
    # s3_local_manager.upload_onnx_slices()  # if not used: comment this line to save S3 costs


def run_inference():
    if not slice_checker.valid_number_of_slices():
        print("First, you need to run a decomposition in slices with the 'decomposition' mode")
        exit(1)

    print("Starting inference:")

    # Load the input data
    img = project_steps.get_preprocessed_input()

    # Run the inference
    first_slice.run(img)
    for slice_index in range(1, constants.NUMBER_OF_SLICES):
        other_slices.run(slice_index)

    # Print the results
    result_printer.print_result()


def max_slice_size_mode():
    if not slice_checker.valid_number_of_slices():
        print("First, you need to run a decomposition in slices with the 'decomposition' mode")
        exit(1)
    max_slice_size_checker.print_max_slice_size()


def payload_per_layer_mode():
    if not constants.NUMBER_OF_SLICES == 1:
        print("For this mode to complete, you need to set NUMBER_OF_SLICES = 1")
        exit(1)
    run_decomposition("payload_per_layer")
    run_inference()
    payload_size_calculator.print_all_payload_sizes()


def payload_per_slice_mode():
    if not slice_checker.valid_number_of_slices():
        print("First, you need to run a decomposition in slices and an inference with the 'basic' mode")
        exit(1)
    elif not os.path.exists(onnxmanager.DICTIONARY_PATH):
        print("First, you need to run an execution with the 'inference' mode")
        exit(1)
    payload_size_calculator.print_payload_sizes()


@profile
def memory_mode():
    run_inference()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='main.py',
        description='This program can perform the model decomposition, the inference, and all the conformity checks '
                    'except the deployment package size check',
        epilog='Text at the bottom of help')  # TODO
    parser.add_argument('mode', choices=['basic', 'decomposition', 'inference', 'max_slice_size', 'payload_per_layer',
                                         'payload_per_slice', 'memory'],
                        help='Choose one of the available modes: basic, decomposition, inference, max_slice_size,'
                             'payload_per_layer, payload_per_slice, memory')
    mode = parser.parse_args().mode
    print("PROJECT: " + constants.PROJECT_NAME + ", " + str(constants.NUMBER_OF_SLICES) + " slice(s)\n")
    if mode == "basic":
        print("MODE: BASIC (DECOMPOSITION AND INFERENCE)\n")
        run_decomposition(mode)
        run_inference()
    elif mode == "decomposition":
        print("MODE: DECOMPOSITION\n")
        run_decomposition(mode)
    elif mode == "inference":
        print("MODE: INFERENCE")
        run_inference()
    elif mode == "payload_per_layer":
        print("MODE: PAYLOAD PER LAYER\n")
        payload_per_layer_mode()
    elif mode == "max_slice_size":
        print("MODE: MAXIMUM SLICE SIZE\n")
        max_slice_size_mode()
    elif mode == "payload_per_slice":
        print("MODE: PAYLOAD PER SLICE\n")
        payload_per_slice_mode()
    elif mode == "memory":
        print("MODE: MEMORY\n")
        memory_mode()
