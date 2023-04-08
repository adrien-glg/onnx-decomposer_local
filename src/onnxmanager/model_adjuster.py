import numpy as np
import onnx

from src.onnxmanager import model_extractor
from src import constants


def add_model_output(loaded_model, model_path, output_name):
    """
    Adds the specified output to the specified ONNX model and saves the new ONNX model to the model path.
    :param loaded_model: Model to which the output will be added.
    :param model_path: Path to which the model will be saved.
    :param output_name: Name of the output to add.
    """
    graph_outputs = []

    for output_index in range(len(loaded_model.graph.output)):
        graph_outputs += [loaded_model.graph.output[output_index].name]

    if output_name not in graph_outputs:
        intermediate_layer_value_info = onnx.helper.ValueInfoProto()
        intermediate_layer_value_info.name = output_name
        loaded_model.graph.output.append(intermediate_layer_value_info)
        onnx.save(loaded_model, model_path)


def adjust_slices(input_lists, output_lists):
    """
    Modifies each slice so that the layer outputs that need to be used by next slices are defined as a model output
    for the slice. This is required so that all non-immediately consumed outputs are saved during the execution
    and used by any of the next slices.
    :param input_lists: List of the matching inputs for each slice.
    :param output_lists: List of the matching output for each slice (one output per slice).
    :return: New list of the matching outputs for each slice.
    """
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

