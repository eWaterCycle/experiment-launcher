from nbformat import NotebookNode

from ewatercycle_experiment_launcher.api.pyewatercycle import notebook


def test_notebook_pcrglobwb():
    setup = {
        "model": {
            "name": "PCRGlobWB",
            "version": "setters"
        },
        "observation": {
            "station_id": "6335020"
        },
        "parameter_set": "pcrglobwb_rhinemeuse_30min",
        "variable": "discharge"
    }
    nb = notebook(setup)

    assert isinstance(nb, NotebookNode)

def test_notebook_marrmotm01():
    setup = {
        "model": {
            "name": "MarrmotM01",
            "version": "2020.11",
            "lumped": True,
        },
        "observation": {
            "station_id": "123456"
        },
        "forcing": "marrmot-m01_example_1989-1992_buffalo-river",
        "variable": "flux_out_Q"
    }
    nb = notebook(setup)

    assert isinstance(nb, NotebookNode)
