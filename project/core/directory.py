# coding: utf-8
import os

_base_dir = None

def get_base_dir():
    """プロジェクトのベースディレクトリのパスを返す関数
    """
    global _base_dir
    if not _base_dir:
        _base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return _base_dir
