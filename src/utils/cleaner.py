import os
import re


def purge(folder, pattern):
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if re.search(pattern, f):
                os.remove(os.path.join(folder, f))


def purge_all_except_pattern(folder, pattern):
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if not re.search(pattern, f):
                os.remove(os.path.join(folder, f))


purge_all_except_pattern("../../1todelete", " ")
