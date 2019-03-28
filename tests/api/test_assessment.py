from nbformat import NotebookNode

from ewatercycle_experiment_launcher.api.assessment import assessment_notebook


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
            'name': 'wflow',
            'grpc4bmi_container': 'wflow-grpc4bmi:latest'
        },
        'assessment': {
            'variable': 'somevarname',
            'index': 42,
            'source': 'grdc',
            'station_id': '6970500'
        }
    }
    nb = assessment_notebook(setup)

    assert isinstance(nb, NotebookNode)

