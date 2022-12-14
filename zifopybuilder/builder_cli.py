"""
Command line interface tools for setting up Python projects that conform to best practices.
"""
import json
import os
import shutil
import subprocess
import sys

import click
import toml

from . import templates

# Load template location
TEMPLATES_PATH = templates.__path__[0]
GITIGNORE_PATH = os.path.join(TEMPLATES_PATH, "gitignore")
PRECOMMIT_PATH = os.path.join(TEMPLATES_PATH, "pre_commit.yaml")
SETTINGS = json.load(
    open(os.path.join(TEMPLATES_PATH, "settings.json"), "r", encoding="utf-8")
)


def copy_templates_to_project():
    """
    Copy the standard templates into the project folder
    """
    gitignore_dst = os.path.join(os.getcwd(), ".gitignore")
    print(f"...copy {GITIGNORE_PATH} to {gitignore_dst}")
    shutil.copy(GITIGNORE_PATH, os.path.join(os.getcwd(), ".gitignore"))

    precommit_dst = os.path.join(os.getcwd(), ".pre-commit-config.yaml")
    print(f"...copy {PRECOMMIT_PATH} to {precommit_dst}")
    shutil.copy(PRECOMMIT_PATH, precommit_dst)


def load_and_update_project_toml():
    """
    Load the project TOML config file and insert default settings
    """
    pyproject_toml = toml.load(open("pyproject.toml", "r", encoding="utf-8"))
    pyproject_toml["tool"]["hatch"]["envs"]["default"]["dependencies"] = SETTINGS["default_quality_tools"]
    pyproject_toml["tool"]["hatch"]["envs"]["default"]["scripts"] = SETTINGS["default_scripts"]
    pyproject_toml["tool"]["hatch"]["envs"]["default"]["post-install-commands"] = SETTINGS["post_install_commands"]
    toml.dump(pyproject_toml, open("pyproject.toml", "w", encoding="utf-8"))


def optimise_project_for_analytical(project_name: str):
    """
    Optimise project for analytical purposes

    Parameters
    ----------
    project_name: str
    """
    click.echo("Creating additional repo structure...")
    os.mkdir("notebooks")
    os.mkdir("data")
    os.mkdir("data/raw")
    os.mkdir("data/interim")
    os.mkdir("data/processed")
    os.mkdir("reports")
    os.mkdir("reports/figures")
    os.mkdir("models")

    click.echo("Installing Jupyter Lab...")
    subprocess.run("hatch run pip install jupyterlab ipykernel", shell=True, check=True)
    subprocess.run(
        f"hatch run python -m ipykernel install --user --name={project_name}",
        shell=True,
        check=True,
    )

    click.echo("Installing Data Science default libs...")
    default_ds_packages = " ".join(SETTINGS["default_ds_packages"])
    subprocess.run(
        f"hatch run pip install {default_ds_packages}", shell=True, check=True
    )


@click.group()
def cli():
    """
    Tool for helping setup a standard Zifo Python project with good defaults pre-installed.
    """
    pass


@cli.command()
@click.option("-n", "--project_name", required=True, type=str)
@click.option("--remote", type=str, default="")
@click.option("--analytical", is_flag=True, show_default=True, default=False)
def setup_project(project_name: str, remote: str, analytical: bool):
    """
    Creates a standard project for Python scripts, applications, web apps, APIs, pipelines,
    or packages. Alternatively, for analytical projects include the --analytical flag

    PROJECT_NAME is the name of the project to be created and the repository
    will be created within the working directory.

    Parameters
    ----------
    project_name: str
        Name of the project to create NOTE: will be converted to lower case!
    remote: str, optional
        The name of a remote repository to add. Ignored if SKIPGIT is TRUE.
    analytical: bool
        Include flag to include additional repository structures, install Jupyter, and install common data sci libs.
    """

    project_name = project_name.lower()
    if os.path.isdir(project_name):
        raise ValueError("Project directory already exists!")

    try:
        click.echo(f"Creating new project {project_name}...")
        subprocess.run(f"hatch new {project_name}", shell=True, check=True)
        os.chdir(project_name)  # Set working directory to the project folder
        click.echo("Installing pre-commit...")
        subprocess.run(f"pip install pre-commit --no-input", shell=True, check=True)
        click.echo("Initiating new git repository...")
        subprocess.run(
            'git init && git add . && git commit -m "Setup project" && git branch -m main',
            shell=True, check=True
        )
        if len(remote) > 0:
            subprocess.run(
                f"git remote add origin {remote}", shell=True, check=True
            )
        click.echo("Copying standard templates to new project...")
        copy_templates_to_project()
        click.echo("Updating project settings with defaults...")
        load_and_update_project_toml()
        click.echo("Creating default environment...")
        subprocess.run("hatch env create", shell=True, check=True)
        if analytical:
            optimise_project_for_analytical(project_name=project_name)

    except subprocess.CalledProcessError as err:
        click.echo(
            click.style(
                f"Errors where encountered whilst creating the project ({err.returncode}) {err.stdout};{err.stderr}",
                bg="black",
                fg="red",
            )
        )
        subprocess.run("hatch env prune", shell=True, check=True)
        os.chdir("..")
        shutil.rmtree(project_name)


if __name__ == "__main__":
    cli()
