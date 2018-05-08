"""Generators for Jupyter noteboook"""
from nbformat import NotebookNode
from nbformat.v4 import new_code_cell, new_notebook


def hello() -> NotebookNode:
    """Generates a Hello world Jupyter notebook"""
    cells = [new_code_cell("print('hello world')")]
    return new_notebook(cells=cells, metadata={'language': 'python'})

