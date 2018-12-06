============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/ewatercycle/ewatercycle_experiment_launcher/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

eWaterCycle Experiment Launcher could always use more documentation, whether as part of the
official eWaterCycle Experiment Launcher docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/ewatercycle/ewatercycle_experiment_launcher/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)


Adding a new notebook type
~~~~~~~~~~~~~~~~~~~~~~~~~~

The web service has an path for each type of notebook.

To add a new type of notebook the following steps must be performed:

1. In `ewatercycle_experiment_launcher/openapi.yaml` file create a new path
    * The http method should be `post`
    * The requestBody should be a json object which includes a `notebook` property of schema type `NotebookRequest`
    * The 200 response should of response type NotebookResponse
    * The default response should of response type ErrorResponse
2. In `ewatercycle_experiment_launcher/api` directory create a file with same name as the chosen path +'.py'
    * Create a `post()` function, using the following template

.. code-block:: python

        from ewatercycle_experiment_launcher.process import process_notebook

        def post(body):
            """Generate notebook and launch it

            Args:
                body: The json POST body as a Python dictionary
            """
            nb = ... # <Add code that generates a nbformat.NotebookNode object>
            return process_notebook(body['notebook'], nb)

3. Write unit tests in `tests/api/` directory

Make a Pull Request after the new notebook type has been implemented and tested.

Get Started!
------------

Ready to contribute? Here's how to set up `ewatercycle_experiment_launcher` for local development.

1. Fork the `ewatercycle_experiment_launcher` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/ewatercycle_experiment_launcher.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv ewatercycle_experiment_launcher
    $ cd ewatercycle_experiment_launcher/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 ewatercycle_experiment_launcher tests
    $ python setup.py test or py.test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.7, 3.4, 3.5 and 3.6, and for PyPy. Check
   https://travis-ci.org/ewatercycle/ewatercycle_experiment_launcher/pull_requests
   and make sure that the tests pass for all supported Python versions.

Release
-------

A reminder for the maintainers on how to release a new version.

1. Make sure tests pass by running::

    $ pytest

2. Bump the version by running::

    $ bumpversion patch # possible: major / minor / patch

3. Update or create an entry for the new version in the `CHANGELOG.md` file
4. Make sure all your changes are committed and pushed
5. Publish to pypi with::

    $ rm -rf dist
    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*

6. Create GitHub release
7. Update DOI in `CITATION.cff` file
