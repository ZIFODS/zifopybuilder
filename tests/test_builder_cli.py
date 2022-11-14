import shutil

import pytest
from click.testing import CliRunner

from zifopybuilder import builder_cli


@pytest.fixture
def fake_filesystem(fs):  # pylint:disable=invalid-name
    """Variable name 'fs' causes a pylint warning. Provide a longer name
    acceptable to pylint for use in tests.
    """
    yield fs


@pytest.mark.parametrize(
    "skipgit,analytical,remote",
    [
        (True, False, ""),
        (True, False, "https://github.com/FAKEUSER/FAKEREPO.git"),
        (True, True, "https://github.com/FAKEUSER/FAKEREPO.git"),
        (False, False, "https://github.com/FAKEUSER/FAKEREPO.git"),
        (False, True, "https://github.com/FAKEUSER/FAKEREPO.git"),
    ],
)
def test_setup_project(skipgit, analytical, remote):
    runner = CliRunner()
    with runner.isolated_filesystem():
        cmd = "setup-project -n TESTPROJECT"
        if skipgit:
            cmd = cmd + " --skipgit"
        if analytical:
            cmd = cmd + " --analytical"
        if remote:
            cmd = cmd + f" --remote {remote}"
        result = runner.invoke(builder_cli.cli, cmd)
        assert result.exit_code == 0
        shutil.rmtree("~/.virtualenvs/testproject")
