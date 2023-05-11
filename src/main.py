import os
import sys
import argparse

from inference import first_slice, other_slices
from jsonmanager import json_manager
from src import onnxmanager
from onnxmanager import lists_builder, model_extractor, model_adjuster
from src.utils import cleaner, result_printer, payload_size_calculator, max_slice_size_checker
from src.s3manager import s3_local_manager
from src import constants

import importlib

project_steps = importlib.import_module(constants.PROJECT_STEPS_MODULE, package=None)


def run_decomposition(selected_mode):
    # Delete the remaining files from previous executions
    cleaner.purge()

    # Decompose the ONNX model in multiple slices
    inputs, outputs = lists_builder.get_built_lists()
    if selected_mode == "payloads_per_layer":
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
    # Load the input data
    img = project_steps.get_preprocessed_input()

    # Run the inference
    first_slice.run(img)
    for slice_index in range(1, constants.NUMBER_OF_SLICES):
        other_slices.run(slice_index)

    # Print the results
    result_printer.print_result()


def max_slice_size_mode():
    if not os.listdir(onnxmanager.SLICES_PATH):
        print("First, you need to run an execution with the 'inference' mode")
        exit(1)
    max_slice_size_checker.print_max_slice_size()


def payloads_per_layer_mode():
    if not os.listdir(onnxmanager.JSON_ROOT_PATH):
        print("First, you need to run an execution with the 'inference' mode")
        exit(1)
    if not constants.NUMBER_OF_SLICES == 1:
        print("For this mode to complete, you need to set NUMBER_OF_SLICES = 1")
        exit(1)
    run_decomposition("payloads_per_layer")
    payload_size_calculator.print_all_payload_sizes()


def payloads_per_slice_mode():
    if not os.listdir(onnxmanager.JSON_ROOT_PATH):
        print("First, you need to run an execution with the 'inference' mode")
    payload_size_calculator.print_payload_sizes()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='main.py',
        description='This program can perform the model decomposition, the inference, and certain conformity checks',
        epilog='Text at the bottom of help')  # TODO
    parser.add_argument('mode', choices=['basic', 'decomposition', 'inference', 'max_slice_size', 'payloads_per_layer',
                                         'payloads_per_slice'],
                        help='Choose one of the available modes: basic, decomposition, inference, max_slice_size,'
                             'payloads_per_layer, or payloads_per_slice')
    mode = parser.parse_args().mode
    if mode == "basic":
        print("MODE: BASIC (DECOMPOSITION AND INFERENCE)\n")
        run_decomposition(mode)
        run_inference()
    if mode == "decomposition":
        print("MODE: DECOMPOSITION\n")
        run_decomposition(mode)
    if mode == "inference":
        print("MODE: INFERENCE")
        run_inference()
    elif mode == "payloads_per_layer":
        print("MODE: PAYLOADS PER LAYER\n")
        payloads_per_layer_mode()
    elif mode == "max_slice_size":
        print("MODE: MAXIMUM SLICE SIZE\n")
        max_slice_size_mode()
    elif mode == "payloads_per_slice":
        print("MODE: PAYLOADS PER SLICE\n")
        payloads_per_slice_mode()
