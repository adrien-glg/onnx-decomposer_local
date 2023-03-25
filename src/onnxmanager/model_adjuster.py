import numpy as np
import onnx

from src.onnxmanager import model_extractor
from src import constants


def add_model_output(loaded_model, model_path, output_name):
    graph_outputs = []

    for output_index in range(len(loaded_model.graph.output)):
        graph_outputs += [loaded_model.graph.output[output_index].name]

    if output_name not in graph_outputs:
        intermediate_layer_value_info = onnx.helper.ValueInfoProto()
        intermediate_layer_value_info.name = output_name
        loaded_model.graph.output.append(intermediate_layer_value_info)
        onnx.save(loaded_model, model_path)


# ADJUST SLICES WITH OUTPUTS NEEDED FOR OTHER SLICES
def adjust_slices(input_lists, output_lists):
    input_lists_flat = list(np.concatenate(input_lists).flat)
    output_lists_flat = list(np.concatenate(output_lists).flat)
    required_outputs = list(set(input_lists_flat) - set(output_lists_flat) - set(constants.INPUT_LIST_START))
    new_output_lists = output_lists

    for slice_index in range(constants.NUMBER_OF_SLICES):
        slice_path = model_extractor.get_slice_path(slice_index)
        model = onnx.load(slice_path)
        nodes = model.graph.node
        for node_index in range(len(nodes)):
            node_output = nodes[node_index].output[0]
            if node_output in required_outputs:
                add_model_output(model, slice_path, node_output)
                if node_output not in new_output_lists[slice_index]:
                    new_output_lists[slice_index] += [node_output]
                required_outputs.remove(nodes[node_index].output[0])

    print("Slices adjusted successfully")
    return new_output_lists

