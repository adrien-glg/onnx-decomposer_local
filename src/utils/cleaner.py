import os
import re

from src import onnxmanager


def purge_pattern(folder, pattern):
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if re.search(pattern, f):
                os.remove(os.path.join(folder, f))


def purge_all_except_pattern(folder, pattern):
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if not re.search(pattern, f):
                os.remove(os.path.join(folder, f))


def purge():
    purge_all_except_pattern(onnxmanager.JSON_ROOT_PATH, "README.md")
    purge_all_except_pattern(onnxmanager.EVENTS_PATH, "README.md")
    purge_pattern(onnxmanager.SLICES_PATH, "")
