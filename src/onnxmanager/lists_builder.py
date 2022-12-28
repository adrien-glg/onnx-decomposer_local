import json

import onnx

from src import onnxmanager
from src import constants


def get_intermediate_outputs(start_layer_index, end_layer_index):
    intermediate_outputs = []
    model = onnx.load(onnxmanager.MODEL_PATH)
    nodes = model.graph.node

    for i in range(start_layer_index, end_layer_index + 1):
        intermediate_outputs += [nodes[i].output[0]]

    return intermediate_outputs


def get_intermediate_inputs(start_layer_index, end_layer_index):
    intermediate_inputs = []
    model = onnx.load(onnxmanager.MODEL_PATH)
    nodes = model.graph.node

    for i in range(start_layer_index, end_layer_index + 1):
        for j in range(len(nodes[i].input)):
            intermediate_inputs += [nodes[i].input[j]]

    return intermediate_inputs


def build_lists():
    input_lists, output_lists, past_outputs = [], [], []

    model = onnx.load(onnxmanager.MODEL_PATH)
    nodes = model.graph.node

    total_nb_of_layers = len(nodes)
    # print("total_nb_of_layers: ", total_nb_of_layers)
    nb_of_layers_per_slice = total_nb_of_layers // constants.NUMBER_OF_SLICES
    top_layer_index = 0
    bottom_layer_index = nb_of_layers_per_slice - 1

    for slice_index in range(constants.NUMBER_OF_SLICES):
        if slice_index == constants.NUMBER_OF_SLICES - 1:
            # Final slice
            output_set = set(constants.OUTPUT_LIST_END)
        else:
            output_set = set([nodes[bottom_layer_index].output[0]])
        input_set = set()

        # (TO BE VERIFIED) A layer can have multiple inputs but only one output
        for layer_index in range(top_layer_index, bottom_layer_index + 1):
            for inp in nodes[layer_index].input:
                if inp in past_outputs:
                    input_set.add(inp)
        input_list = list(input_set)
        input_list.sort()
        input_lists += [input_list]

        # Output set correction (add missing outputs):
        intermediate_inputs = get_intermediate_inputs(top_layer_index, bottom_layer_index)
        for layer_index in range(top_layer_index, bottom_layer_index + 1):
            if nodes[layer_index].output[0] not in intermediate_inputs:
                output_set.add(nodes[layer_index].output[0])
        # END Output set correction

        output_list = list(output_set)
        output_list.sort()
        output_lists += [output_list]

        intermediate_outputs = get_intermediate_outputs(top_layer_index, bottom_layer_index)
        past_outputs += intermediate_outputs

        top_layer_index += nb_of_layers_per_slice
        bottom_layer_index += nb_of_layers_per_slice

    # First slice:
    input_lists[0] = constants.INPUT_LIST_START

    return input_lists, output_lists
