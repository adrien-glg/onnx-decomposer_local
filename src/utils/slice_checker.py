import os

from src import constants
from src import onnxmanager


def valid_number_of_slices():
    requested_number_of_slices = constants.NUMBER_OF_SLICES
    number_of_generated_slices = len(os.listdir(onnxmanager.SLICES_PATH))
    return requested_number_of_slices == number_of_generated_slices
