# zifopybuilder

---

**This project is under activate development**

The ZifoPyBuilder is a command line tool for setting up Zifo Python projects that conform to best practices. The tool
uses <a href="https://python-poetry.org/">Poetry</a>, a popular library for Python project management.
**ZifoPyBuilder assumes you are setting up a new project**. If you have inherited a code repository, then use the standards 
guidelines available on Teams as guidance on enforcing the correct standards and installing quality control tools.

ZifoPyBuilder sets up quality tools and standards using a set of templates, found in zifopybuilder/templates. The templates
include:

- gitignore file - preventing the pollution of git repositories with large data files, IDE metadata, and other unwanted items
- pre-commit YAML - defines a set of pre-commit hooks to be run when making commits to your local branch, checking code quality and formatting
- Settings JSON - defaults inserted into each Project TOML config file and installing default packages for analytical projects

**Table of Contents**

- [Release Notes](#releasenotes)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [License](#license)

## Release Notes

- v0.2.0 - Refactor to use Poetry for dependency management and packaging
- v0.1.0 - pre-release; tested in isolated environment. Can be used internally but feedback and additional testing needed.
- v0.0.1 - pre-release; functional but not tested

## Installation

**Requires poetry is installed on your local machine within your global Python environment**

```console
pip install poetry
```

Installation is via the GitHub page. Version v0.2.0 will make Python wheels available from the Github repo release page.

**Make sure to install zifopybuilder in your global environment**

Otherwise, install using:

```console
pip install git+https://github.com/ZIFODS/zifopybuilder.git
```

Alternatively, clone the repository to your local machine and build the package using the following command within the project directory:

```console
poetry build
```

This will generate a Python wheel inside the `dist` folder. Install the package using this wheel with:

```console
pip install dist/zifopybuilder-#.#.#-py3-none-any.whl
```

Where #.#.# is the version number.

## Quickstart

**Note: This tool is designed to be used in a new project. If you have inherited a project, 
please use the standards guidelines. When creating projects with ZifoPyBuilder, you will need to 
commit to add an empty remote repository.**

Once installed, the tool can be run from the command line anywhere using the `zifopybuilder` command. The new project
will be generated within your current working directory creating a new directory named after your project.

You can use the `-help` flag to see more details about how to use the tool:

```console
zifopybuilder --help
```

To create a standard project called "myproject" run

```console
zifopybuilder setup-project -n myproject
```

If you have already setup a remote repository, you can include the name of the remote repo:

```console
zifopybuilder setup-project -n myproject --remote https://github.com/ZIFODS/myproject.git
```

If the project you're setting up is for an analytical project, as opposed to a Python package, app, or pipeline, then use the `--analytical` flag:

```console
zifopybuilder setup-project -n myproject --analytical
```

This will create an extended repository structure designed for a data analysis workflow, will install Pandas, Numpy, Matplotlib, Seaborn, Scikit-Learn,
and Statsmodels, and will setup Jupyter lab.

Once a project is setup, use `poetry shell` to enter your virtual environment and `poetry run` to run scripts.

## License

`zifopybuilder` is distributed under the terms of the [0BSD](https://spdx.org/licenses/0BSD.html) license.
