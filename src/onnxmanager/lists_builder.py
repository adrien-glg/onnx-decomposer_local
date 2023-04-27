import onnx

from src import onnxmanager
from src import constants


def get_all_outputs():
    """
    Returns a list of the outputs of all the layers in the ONNX model.
    :return:
    """
    all_outputs = []
    model = onnx.load(onnxmanager.MODEL_PATH)
    nodes = model.graph.node
    total_nb_of_layers = len(nodes)

    for i in range(total_nb_of_layers):
        all_outputs += [nodes[i].output[0]]
    all_outputs = [all_outputs]

    return all_outputs


def get_intermediate_outputs(start_layer_index, end_layer_index):
    """
    Returns a list of the outputs encountered between 2 layers in the ONNX model, output of the last layer included.
    :param start_layer_index:
    :param end_layer_index:
    :return:
    """
    intermediate_outputs = []
    model = onnx.load(onnxmanager.MODEL_PATH)
    nodes = model.graph.node

    for i in range(start_layer_index, end_layer_index + 1):
        intermediate_outputs += [nodes[i].output[0]]

    return intermediate_outputs


def get_intermediate_inputs(start_layer_index, end_layer_index):
    """
    Returns a list of the inputs encountered between 2 layers in the ONNX model, inputs of the last layer included.
    :param start_layer_index:
    :param end_layer_index:
    :return:
    """
    intermediate_inputs = []
    model = onnx.load(onnxmanager.MODEL_PATH)
    nodes = model.graph.node

    for i in range(start_layer_index, end_layer_index + 1):
        for j in range(len(nodes[i].input)):
            intermediate_inputs += [nodes[i].input[j]]

    return intermediate_inputs


def get_built_lists():
    """
    Creates the input and output lists required by each slice of the ONNX model. These lists depend on the slicing
    pattern selected, i.e., the chosen number of slices.
    :return: List of the matching inputs for each slice and list of the matching output for each slice (possibly
    multiple inputs per slice, but always one output per slice).
    """
    print("PROJECT: " + constants.PROJECT_NAME + ", " + str(constants.NUMBER_OF_SLICES) + " slice(s)\n")
    input_lists, output_lists, past_outputs = [], [], []
    model = onnx.load(onnxmanager.MODEL_PATH)
    nodes = model.graph.node

    total_nb_of_layers = len(nodes)
    nb_of_layers_per_slice = total_nb_of_layers // constants.NUMBER_OF_SLICES
    top_layer_index = 0
    bottom_layer_index = nb_of_layers_per_slice - 1
    for slice_index in range(constants.NUMBER_OF_SLICES):
        if slice_index == constants.NUMBER_OF_SLICES - 1:
            output_set = set(constants.OUTPUT_LIST_END)
        else:
            output_set = set([nodes[bottom_layer_index].output[0]])

        input_set = set()
        for layer_index in range(top_layer_index, bottom_layer_index + 1):
            for inp in nodes[layer_index].input:
                if inp in past_outputs:
                    input_set.add(inp)
        input_list = sorted(list(input_set))
        input_lists += [input_list]

        intermediate_inputs = get_intermediate_inputs(top_layer_index, bottom_layer_index)
        intermediate_outputs = get_intermediate_outputs(top_layer_index, bottom_layer_index)
        for layer_index in range(top_layer_index, bottom_layer_index + 1):
            if nodes[layer_index].output[0] not in intermediate_inputs:
                output_set.add(nodes[layer_index].output[0])

        output_list = sorted(list(output_set))
        output_lists += [output_list]
        past_outputs += intermediate_outputs
        top_layer_index += nb_of_layers_per_slice
        bottom_layer_index += nb_of_layers_per_slice

    input_lists[0] = constants.INPUT_LIST_START

    print("Lists built successfully")
    return input_lists, output_lists
