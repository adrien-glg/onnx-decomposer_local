import os
import shutil

import onnxmanager
from onnxmanager import lists_builder, model_extractor, model_refactorer
from inference import other_slices, mobiledet_first_slice, efficientdet_first_slice
from jsonmanager import json_manager, payload_size_calculator
import constants


if __name__ == '__main__':

    # Do not forget to delete all files from previous executions
    # if os.path.exists(onnxmanager.JSON_ROOT_PATH):
    #     shutil.rmtree(onnxmanager.JSON_ROOT_PATH)

    inputs, outputs = lists_builder.build_lists()

    if os.path.exists(onnxmanager.SLICES_PATH):
        shutil.rmtree(onnxmanager.SLICES_PATH)
    model_extractor.extract_model_slices(inputs, outputs)

    outputs = model_refactorer.refactor_slices(inputs, outputs)

    payloads_sizes = payload_size_calculator.get_payloads_sizes(outputs)
    print(payloads_sizes)

    pretty_payloads_sizes = payload_size_calculator.get_pretty_payloads_sizes(outputs)
    print(pretty_payloads_sizes)

    # MOBILEDET:
    # mobiledet_first_slice.run(outputs)
    #
    # for slice_index in range(1, constants.NUMBER_OF_SLICES):
    #     other_slices.run(slice_index, inputs, outputs)
    #     print("Slice " + str(slice_index) + " execution completed successfully")
    #
    # result = json_manager.get_payload_content("TFLite_Detection_PostProcess")
    # print("\nRESULTS:")
    # print(result[0][0])
    # END MOBILEDET

    # EFFICIENTDET:
    # efficientdet_first_slice.run(outputs)
    #
    # for slice_index in range(1, constants.NUMBER_OF_SLICES):
    #     print(slice_index)
    #     other_slices.run(slice_index, inputs, outputs)
    #
    # result = jsonmanager.get_payload_content("detections:0")
    # print("\nRESULTS:")
    # print(result[0][0])
    # END EFFICIENTDET
