import textwrap

from nbformat import NotebookNode
from nbformat.v4 import new_markdown_cell, new_code_cell, new_notebook

from ewatercycle_experiment_launcher.generate import PY3_META
from ewatercycle_experiment_launcher.process import process_notebook


def notebook(setup) -> NotebookNode:
    """Generates a Jupyter notebook"""
    welcome = textwrap.dedent("""
        # **Welcome to the eWaterCycle experiment notebook**

        This notebook was generated by the eWaterCycle experiment launcher.

        We will use GRDC data for comparison between the model simulation and the observations.

        In this example notebook we run a hydrology model using [ewayercycle](https://github.com/eWaterCycle/ewatercycle).
        """)
    cells = [
        new_markdown_cell(welcome),
        new_code_cell(textwrap.dedent("""\
            import ewatercycle.parameter_sets
            import ewatercycle.forcing
            import ewatercycle.models
            import ewatercycle.observation.grdc
            import ewatercycle.analysis\
        """)),
    ]

    if 'parameter_set' in setup:
        cells += [
            new_markdown_cell('## Load parameter set'),
            new_code_cell(textwrap.dedent(f"""\
                parameter_set = ewatercycle.parameter_sets.get_parameter_set("{setup['parameter_set']}")
                parameter_set\
            """)),
        ]
    if 'forcing' in setup:
        forcing = setup['forcing']
        if not forcing.startswith('/'):
            # TODO make forcing_root_dir configurable
            forcing_root_dir = '/mnt/data/forcing'
            forcing = forcing_root_dir + '/' + forcing
        cells += [
            new_markdown_cell('## Load forcing data'),
            # TODO prepend a root dir to forcing dir
            new_code_cell(textwrap.dedent(f"""\
                forcing = ewatercycle.forcing.load("{setup['forcing']}")
                forcing\
            """)),
        ]

    cells += [
        new_markdown_cell('## Setting up the model'),
    ]

    model_name = setup['model']['name']
    model_version = setup['model']['version']
    if 'parameter_set' in setup and 'forcing' in setup:
        cells += [
            new_code_cell(textwrap.dedent(f"""\
                model = ewatercycle.models.{model_name}(version="{model_version}", parameter_set=parameter_set, forcing=forcing)\
            """)),
        ]
    elif 'forcing' in setup:
        cells += [
            new_code_cell(textwrap.dedent(f"""\
                model = ewatercycle.models.{model_name}(version="{model_version}", forcing=forcing)\
            """)),
        ]
    elif 'parameter_set' in setup:
        cells += [
            new_code_cell(textwrap.dedent(f"""\
                model = ewatercycle.models.{model_name}(version="{model_version}", parameter_set=parameter_set)\
            """)),
        ]
    else:
        cells += [
            new_code_cell(textwrap.dedent(f"""\
                model = ewatercycle.models.{model_name}(version="{model_version}")\
            """)),
        ]

    observation = setup['observation']
    cells += [
        new_markdown_cell('Current parameters of model.'),
        new_code_cell(textwrap.dedent("""\
            model.parameters\
        """)),
        new_markdown_cell('Pass on or more parameters with a custom value to the setup method to overwrite.'),
        new_code_cell(textwrap.dedent(f"""\
            cfg_file, cfg_dir = model.setup()

            model.initialize(cfg_file)\
        """)),
        new_markdown_cell('## Observation'),
        new_code_cell(textwrap.dedent(f"""\
            grdc_station_id = {observation['station_id']}
            observations, station_metadata = ewatercycle.observation.grdc.get_grdc_data(
                station_id=grdc_station_id,
                start_time=model.start_time_as_isostr,
                end_time=model.end_time_as_isostr,
                column="GRDC",
            )\
        """)),
        new_markdown_cell('## Running the model'),
    ]
    if 'lumped' in setup['model'] and setup['model']['lumped']:
        cells += [
            new_code_cell(textwrap.dedent(f"""\
                output = []
                while model.time < model.end_time:
                    model.update()
                    # Lumped models only have single value
                    discharge = model.get_value("{setup['variable']}")[0]
                    output.append(discharge)\
            """)),
        ]
    else:
        if 'model_location' in observation:
            model_location = observation['model_location']
            cells += [
                new_markdown_cell(f'''Get "{setup['variable']}" at model location equivalent to GRDC station location.'''),
                new_code_cell(textwrap.dedent(f"""\
                    grdc_latitude = {model_location['latitude']}
                    grdc_longitude = {model_location['longitude']}\
                """)),
            ]
        else:
            cells += [
                new_markdown_cell(f'''Get "{setup['variable']}" at GRDC station.'''),
                new_code_cell(textwrap.dedent(f"""\
                    grdc_latitude = station_metadata['grdc_latitude_in_arc_degree']
                    grdc_longitude = station_metadata['grdc_longitude_in_arc_degree']\
                """)),
            ]

        cells += [
            new_code_cell(textwrap.dedent(f"""\
                output = []
                while model.time < model.end_time:
                    model.update()
                    discharge = model.get_value_at_coords("{setup['variable']}", lat=[grdc_latitude], lon=[grdc_longitude])
                    output.append(discharge)\
            """)),
            ]

    cells += [
        new_markdown_cell('## Analysis'),
        # TODO join simulation and observation based on date index, instead of on size
        new_code_cell(textwrap.dedent(f"""\
            combined_discharge = observations
            combined_discharge["{model_name}"] = output

            ewatercycle.analysis.hydrograph(
                discharge=combined_discharge,
                reference="GRDC",
            )\
        """)),
        new_markdown_cell('## Clean up'),
        new_code_cell(textwrap.dedent("""\
            model.finalize()\
        """)),
    ]
    return new_notebook(cells=cells, metadata=PY3_META)

def post(body):
    """Generate notebook and launch it

    Args:
        body: The json POST body as a Python object
    """
    nb = notebook(body['setup'])
    return process_notebook(body['notebook'], nb)
