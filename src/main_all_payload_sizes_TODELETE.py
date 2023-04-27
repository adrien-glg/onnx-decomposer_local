import shutil
import onnx

import onnxmanager
from inference import first_slice, other_slices
from jsonmanager import json_manager
from onnxmanager import lists_builder, model_extractor, model_adjuster
from src.utils import cleaner, result_printer, size_helper, payload_size_calculator
from src import constants

import importlib
project_steps = importlib.import_module(constants.PROJECT_STEPS_MODULE, package=None)


# THE FOLLOWING CODE ONLY WORKS WITH NUMBER_OF_SLICES=1
if __name__ == '__main__':

    # Delete the remaining files from previous executions
    cleaner.purge()

    inputs, outputs = lists_builder.get_built_lists()

    outputs = lists_builder.get_all_outputs()

    # INSTEAD OF RUNNING THE CODE BELOW ("LASTING CODE SNIPPET"), DO:
    # move mobiledet_all_outputs.onnx to the models/mobiledet/slices/ folder
    # rename this file to mobiledet_slice0.onnx

    # LASTING CODE SNIPPET
    model_adjuster.add_all_model_outputs(outputs)
    # END LASTING CODE SNIPPET

    # Create the first event (only to prepare a future execution with AWS)
    json_manager.make_and_export_event(0, inputs, outputs)

    img = project_steps.get_preprocessed_input()
    first_slice.run(img, inputs, outputs)

    # Print the results
    result_printer.print_result()

    # PAYLOAD SIZES
    print("\nALL PAYLOAD SIZES:")
    payload_sizes = payload_size_calculator.get_all_payload_sizes(outputs)
    # print(payload_sizes)

    pretty_payload_sizes = size_helper.get_pretty_sizes(payload_sizes)
    print(pretty_payload_sizes)
