import ntpath
from pathlib import Path
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)