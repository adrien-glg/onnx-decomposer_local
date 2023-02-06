import shutil
import onnx

import onnxmanager
from inference import first_slice, other_slices
from jsonmanager import json_manager
from onnxmanager import lists_builder, model_extractor, model_refactorer
from src.utils import cleaner
from src.utils import sizes_helper, payload_size_calculator
from src import constants

import importlib
project_steps = importlib.import_module(constants.PROJECT_STEPS_MODULE, package=None)


# THE FOLLOWING CODE ONLY WORKS WITH NUMBER_OF_SLICES=1
if __name__ == '__main__':

    cleaner.purge_all_except_pattern(onnxmanager.JSON_ROOT_PATH, "README.md")
    cleaner.purge_all_except_pattern(onnxmanager.EVENTS_PATH, "README.md")

    inputs, outputs = lists_builder.build_lists()

    outputs = [lists_builder.get_all_outputs()]

    # INSTEAD OF RUNNING THE CODE BELOW ("LASTING CODE SNIPPET"), DO:
    # move mobiledet_all_outputs.onnx to the models/mobiledet/slices/ folder
    # rename this file to mobiledet_slice0.onnx

    # LASTING CODE SNIPPET
    cleaner.purge(onnxmanager.SLICES_PATH, "")
    model = onnx.load(onnxmanager.MODEL_PATH)
    modified_model_path = model_extractor.get_slice_path(0)
    for i in range(len(outputs[0])):
        model_refactorer.add_model_output(model, modified_model_path, outputs[0][i])
    # END LASTING CODE SNIPPET

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

    # PAYLOADS SIZES
    print("\nALL PAYLOADS SIZES:")
    payloads_sizes = payload_size_calculator.get_all_payloads_sizes(outputs)
    # print(payloads_sizes)

    pretty_payloads_sizes = sizes_helper.get_pretty_sizes(payloads_sizes)
    print(pretty_payloads_sizes)
