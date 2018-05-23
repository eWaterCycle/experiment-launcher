from nbformat import NotebookNode

from ewatercycle_experiment_launcher.api.opendap import notebook


def test_notebook():
    opendap_url = 'https:/thredds.server.example.com/opendap/bla.nc'
    nb = notebook(opendap_url)

    assert isinstance(nb, NotebookNode)

