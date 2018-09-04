from nbformat import NotebookNode

from ewatercycle_experiment_launcher.api.bmi import bmi_notebook


def test_bmi_notebook():
    setup = {
        'config': {
            'format': 'ini',
            'url': 'https://example.com/config.ini'
        },
        'datafiles': {
            'format': 'svn',
            'url': 'https://example.com/svn/someproject/trunk'
        },
        'model': {
            'grpc4bmi_container': 'wflow-grpc4bmi:latest'
        },
        'plotting': {
            'variable': 'somevarname',
            'index': 42
        }
    }
    nb = bmi_notebook(setup)

    assert isinstance(nb, NotebookNode)

