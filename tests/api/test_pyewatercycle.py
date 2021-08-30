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
    nb = notebook(setup, '/mnt/data/forcing')

    assert isinstance(nb, NotebookNode)
    assert len(nb['cells']) == 25


def test_notebook_pcrglobwb_with_forcing():
    setup = {
        "model": {
            "name": "PCRGlobWB",
            "version": "setters"
        },
        "observation": {
            "station_id": "6335020"
        },
        "parameter_set": "pcrglobwb_rhinemeuse_30min",
        "forcing": "pcrglobwb_ERA5_1990-1990_rhinemeuse",
        "variable": "discharge"
    }
    nb = notebook(setup, '/mnt/data/forcing')

    assert isinstance(nb, NotebookNode)
    assert len(nb['cells']) == 27


def test_notebook_pcrglobwb_with_location():
    setup = {
        "model": {
            "name": "PCRGlobWB",
            "version": "setters"
        },
        "observation": {
            "station_id": "6335020",
            "model_location": {
                "longitude": 6.395395,
                "latitude": 51.756918
            }
        },
        "parameter_set": "pcrglobwb_rhinemeuse_30min",
        "variable": "discharge"
    }
    nb = notebook(setup, '/mnt/data/forcing')

    assert isinstance(nb, NotebookNode)
    assert len(nb['cells']) == 25


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
    nb = notebook(setup, '/mnt/data/forcing')

    assert isinstance(nb, NotebookNode)
    assert len(nb['cells']) == 23


def test_notebook_marrmotm01_without_forcing():
    setup = {
        "model": {
            "name": "MarrmotM01",
            "version": "2020.11",
            "lumped": True,
        },
        "observation": {
            "station_id": "123456"
        },
        "variable": "flux_out_Q"
    }
    nb = notebook(setup, '/mnt/data/forcing')

    assert isinstance(nb, NotebookNode)
    assert len(nb['cells']) == 21
