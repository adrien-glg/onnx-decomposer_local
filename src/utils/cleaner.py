import os
import re

from src import onnxmanager


def purge_pattern(folder, pattern):
    """
    Deletes all the files located in the specified folder, which match the specified pattern.
    :param folder: Folder in which the files are located.
    :param pattern: Pattern that need to be matched by the files we want to delete.
    :return:
    """
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if re.search(pattern, f):
                os.remove(os.path.join(folder, f))


def purge_all_except_pattern(folder, pattern):
    """
    Deletes all the files located in the specified folder, except those which match the specified pattern.
    :param folder: Folder in which the files are located.
    :param pattern: Pattern that need to be matched by the files we want to keep.
    :return:
    """
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if not re.search(pattern, f):
                os.remove(os.path.join(folder, f))


def purge():
    """
    Deletes all the files required to start a clean execution.
    """
    purge_all_except_pattern(onnxmanager.JSON_ROOT_PATH, "README.md")
    purge_all_except_pattern(onnxmanager.EVENTS_PATH, "README.md")
    purge_pattern(onnxmanager.SLICES_PATH, "")
