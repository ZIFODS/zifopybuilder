# zifopybuilder

[![PyPI - Version](https://img.shields.io/pypi/v/zifopybuilder.svg)](https://pypi.org/project/zifopybuilder)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zifopybuilder.svg)](https://pypi.org/project/zifopybuilder)

---

**This project is under activate development**

The ZifoPyBuilder is a command line tool for setting up Zifo Python projects that conform to best practices. The tool
uses <a href="https://hatch.pypa.io/latest/config/hatch/">hatch</a>, the PyPA supported library for Python project management.

ZifoPyBuilder sets up quality tools and standards using a set of templates, found in zifopybuilder/templates. The templates
include:

- gitignore file - preventing the polution of git repositories with large data files, IDE metadata, and other unwanted items
- pre-commit YAML - defines a set of pre-commit hooks to be run when making commits to your local branch, checking code quality and formatting
- Settings JSON - defaults inserted into each Project TOML config file, automatically installing quality checking tools and pre-commit, setting
  up command line scripts that can be run with `hatch run {SCRIPT NAME}`, and installing default packages for analytical projects

**Table of Contents**

- [Release Notes](#releasenotes)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [License](#license)

## Release Notes

- v0.0.1 - pre-release; functional but not tested

## Installation

**Requires hatch is installed on your local machine within your global Python environment**

```console
pip install hatch
```

Installation is via the GitHub page. Version v0.0.2 will make Python wheels avaiable from the Github repo release page.

**Make sure to install zypybuilder in your global environment**

Otherwise, install using:

```console
pip install git+https://github.com/ZIFODS/zifopybuilder.git
```

Alternatively, clone the repository to your local machine and build the package using the following command within the project directory:

```console
hatch build
```

This will generate a Python wheel inside the `dist` folder. Install the package using this wheel with:

```console
pip install dist/zifopybuilder-#.#.#-py3-none-any.whl
```

Where #.#.# is the version number.

## Quickstart

Once installed, the tool can be run from the command line anywhere using the `zypybuilder` command. The new project
will be generated within your current working directory creating a new directory named after your project.

You can use the `-help` flag to see more details about how to use the tool:

```console
zypybuilder -help
```

To create a standard project called "myproject" run

```console
zypybuilder -n myproject
```

By default, a new git repo will be initialised, to prevent this, use the `--skipgit` flag:

```console
zypybuilder -n myproject --skipgit
```

If you have already setup a remote repository, you can include the name of the remote repo:

```console
zypybuilder -n myproject --remote https://github.com/ZIFODS/myproject.git
```

If the project you're setting up is for an analytical project, as opposed to a Python package, app, or pipeline, then use the `--analytical` flag:

```console
zypybuilder -n myproject --analytical
```

This will create an extended repository structure designed for a data analysis workflow, will install Pandas, Numpy, Matplotlib, Seaborn, Scikit-Learn,
and Statsmodels, and will setup Jupyter lab.

Once a project is setup, use `hatch shell` to enter your virtual environment and `hatch run` to run scripts.

## License

`zifopybuilder` is distributed under the terms of the [0BSD](https://spdx.org/licenses/0BSD.html) license.
