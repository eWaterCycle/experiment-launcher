from nbformat import NotebookNode

from ewatercycle_experiment_launcher.api.threeclickscience import notebook


def test_notebook():
    setup = {
        'model': 'SomeModel',
        'region': 'my-test-region',
        'period': {
            'start': '1970-01-01',
            'end': '2018-01-01'
        }
    }
    nb = notebook(setup)

    assert isinstance(nb, NotebookNode)

