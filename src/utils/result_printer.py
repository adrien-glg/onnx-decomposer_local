from src import constants

import importlib
project_steps = importlib.import_module(constants.PROJECT_STEPS_MODULE, package=None)


def print_result():
    result = project_steps.get_result()
    print("Inference successful")
    print("\nRESULTS:")
    print(result)
