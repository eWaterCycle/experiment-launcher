import textwrap

from nbformat import NotebookNode
from nbformat.v4 import new_markdown_cell, new_code_cell, new_notebook

from ewatercycle_experiment_launcher.auth import requires_auth
from ewatercycle_experiment_launcher.generate import PY3_META
from ewatercycle_experiment_launcher.process import process_notebook


def bmi_notebook(setup) -> NotebookNode:
    """Generates a Jupyter notebook"""
    welcome = textwrap.dedent("""
        # Welcome

        This notebook was generated by the eWaterCycle experiment launcher.

        The notebook runs a hydrology model using [grpc4bmi](https://github.com/eWaterCycle/grpc4bmi).

        """)
    cells = [
        new_markdown_cell(welcome),
        new_code_cell('from ewatercycle.parametersetdb import ParameterSet, DATAFILES_FORMATS, CONFIG_FORMATS'),
        new_code_cell(textwrap.dedent("""\
            # Prepare input
            parameter_set = ParameterSet(
                DATAFILES_FORMATS['{0}']('{1}'),
                CONFIG_FORMATS['{2}']('{3}')
            )
            parameter_set.save_datafiles('./input')""".format(setup['datafiles']['format'], setup['datafiles']['url'],
                                                              setup['config']['format'], setup['config']['url'])
                                      )),
        new_code_cell(textwrap.dedent("""\
            # Overwrite items in config file
            # parameter_set.config['...']['...'] = '...'
            """)),
        new_code_cell(textwrap.dedent("""\
            # The model inside a BMI Docker container expects the datafiles in the /data/input directory,
            # the config file must be adjusted to that

            # For PCR-GLOBWB model the input and output directory must be set with
            # parameter_set.config['globalOptions']['inputDir'] = '/data/input'
            # parameter_set.config['globalOptions']['outputDir'] = '/data/output'

            # For wflow model the config file must be set with
            # parameter_set.config['model']['configfile'] = /data/input/config.cfg'

            # For Walrus model the data file must be set with
            # import os;parameter_set.config['data'] = '/data/input/' + os.listdir('input')[0]
            """)),
        new_code_cell(textwrap.dedent("""\
            # Save config file
            parameter_set.save_config('config.cfg')""")),
        new_code_cell('from grpc4bmi.bmi_client_docker import BmiClientDocker'),
        new_code_cell(textwrap.dedent("""\
            # Startup model
            model = BmiClientDocker(image={0},
                                    input_dir="./input",
                                    output_dir="./output")
            model.initialize('config.cfg')""".format(setup['model']['grpc4bmi_container'])
                                      )),
        new_code_cell(textwrap.dedent("""\
            # Evolve model
            tend = model.get_end_time()
            model.update_until(tend)""")),
        new_code_cell(textwrap.dedent("""\
            # Plot first variable 
            variable = model.get_output_var_names()[0]
            vals = model.get_value(variable)
            unit = model.get_var_units(variable)""".format(setup['var2plot'])
                                      )),
        new_code_cell(textwrap.dedent("""\
            import matplotlib.pyplot as plt
            import numpy
            import numpy.ma as ma
            missval = -999.
            X, Y = numpy.arange(vals.shape[1]), numpy.arange(vals.shape[0])
            Z = ma.masked_where(vals == missval, vals)
            plt.title(variable + '[' + unit + ']')
            plt.pcolormesh(X,Y,Z)
            plt.colorbar()
            plt.plot()"""
                                      )),
        new_code_cell(textwrap.dedent("""\
            # Stop the Docker container
            del model"""))
    ]
    return new_notebook(cells=cells, metadata=PY3_META)


@requires_auth
def post(request):
    """Generate notebook and launch it

    Args:
        request: The json POST body as a Python object
    """
    nb = bmi_notebook(request['setup'])
    return process_notebook(request['notebook'], nb)
