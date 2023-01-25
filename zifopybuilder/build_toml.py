from typing import List

import toml


def create_new_project_toml(
        toml_file: str,
        name: str,
        description: str,
        authors: List[str],
        version: str = "0.0.1",
        license_name: str = "MIT",
        readme: str = "README.md",
        python_version: str = ">=3.10,<3.12"
):
    dependencies = {
        "python": python_version
    }
    toml_dict = {
        "tool": {
            "poetry": {
                "name": name,
                "version": version,
                "description": description,
                "authors": authors,
                "license": license_name,
                "readme": readme,
                "dependencies": dependencies,
                "dev-dependencies": {
                    "pytest": "*",
                    "pytest-cov": "*",
                    "mypy": "*",
                    "pre-commit": "*"
                }
            }
        },
        "build-system": {
            "requires": ["poetry-core"],
            "build-backend": "poetry.core.masonry.api"
        }
    }
    with open(toml_file, "w") as f:
        toml.dump(toml_dict, f)
