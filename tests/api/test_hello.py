from nbformat import NotebookNode

from ewatercycle_experiment_launcher.api.hello import notebook


def test_notebook():
    nb = notebook()

    assert isinstance(nb, NotebookNode)
