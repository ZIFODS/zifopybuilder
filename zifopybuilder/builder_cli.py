"""
Command line interface tools for setting up Python projects that conform to best practices.
"""
import json
import os
import shutil
import subprocess

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
    shutil.copyfile(GITIGNORE_PATH, ".gitignore")
    shutil.copyfile(PRECOMMIT_PATH, ".pre-commit-config.yaml")


def load_and_update_project_toml():
    """
    Load the project TOML config file and insert default settings
    """
    pyproject_toml = toml.load(open("pyproject.toml", "r", encoding="utf-8"))
    pyproject_toml["tool"]["hatch"]["envs"]["default"]["dependencies"] = SETTINGS[
        "default_quality_tools"
    ]
    pyproject_toml["tool"]["hatch"]["envs"]["default"]["scripts"] = SETTINGS[
        "default_scripts"
    ]
    pyproject_toml["tool"]["hatch"]["envs"]["default"][
        "post-install-commands"
    ] = SETTINGS["post_install_commands"]
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
@click.option("--skipgit", is_flag=True, show_default=True, default=False)
@click.option("--remote", type=str, default="")
@click.option("--analytical", is_flag=True, show_default=True, default=False)
def setup_project(project_name: str, skipgit: bool, remote: str, analytical: bool):
    """
    Creates a standard project for Python scripts, applications, web apps, APIs, pipelines,
    or packages. Alternatively, for analytical projects include the --analytical flag

    PROJECT_NAME is the the name of the project to be created and the repository
    will be created within the working directory.

    Parameters
    ----------
    skipgit: bool
        Include flag to prevent initialising a new git repository
    remote: str, optional
        The name of a remote repository to add. Ignored if SKIPGIT is TRUE.
    analytical: bool
        Include flag to include additional repository structures, install Jupyter, and install common data sci libs.
    """
    if os.path.isdir(project_name):
        raise ValueError("Project directory already exists!")

    click.echo(f"Creating new project {project_name}...")
    subprocess.run(f"hatch new {project_name}", shell=True, check=True)
    os.chdir(project_name)  # Set working directory to the project folder

    if not skipgit:
        click.echo("Initiating new git repository...")
        try:
            subprocess.run("git init", shell=True, check=True)
            if len(remote) > 0:
                subprocess.run(
                    f"git remote add origin {remote}", shell=True, check=True
                )
        except subprocess.CalledProcessError as err:
            click.echo(
                click.style(
                    f"Unable to initiate git repository. Has git been installed? ({err.returncode}) {err.stderr}",
                    bg="black",
                    fg="red",
                )
            )
            skipgit = True

    click.echo("Copying standard templates to new project...")
    copy_templates_to_project()
    click.echo("Updating project setting with defaults...")
    load_and_update_project_toml()
    click.echo("Creating default environment...")
    subprocess.run("hatch env create", shell=True, check=True)

    if analytical:
        optimise_project_for_analytical(project_name=project_name)


if __name__ == "__main__":
    cli()
