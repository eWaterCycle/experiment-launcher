from nbformat import NotebookNode

from ewatercycle_experiment_launcher.api.bmi import bmi_notebook


def test_bmi_notebook():
    setup = {
        'model': 'wflow',
        'parameterset': 'wflow_rhine_sbm',
        'docker': 'wflow-grpc4bmi:latest',
        'var2plot': 'SurfaceRunoff',
        'step': 100
    }
    nb = bmi_notebook(setup)

    assert isinstance(nb, NotebookNode)

