import os

_base_dir = None

def get_base_dir():
    global _base_dir
    if not _base_dir:
        _base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return _base_dir