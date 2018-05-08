# -*- coding: utf-8 -*-

"""Console script for ewatercycle_experiment_launcher."""
import sys
import click


@click.command()
@click.Argument
def main(args=None):
    """Console script for ewatercycle_experiment_launcher."""
    click.echo("Replace this message by putting your code into "
               "ewatercycle_experiment_launcher.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")


    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
