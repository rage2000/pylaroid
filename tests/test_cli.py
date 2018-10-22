from click.testing import CliRunner

from pylaroid import __version__
from pylaroid.console_script import cli_frontend


def test_version(caplog):
    """
    Testing printing version
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():

        # Default verbosity
        result = runner.invoke(cli_frontend, ['--version'])

        assert result.exit_code == 0
        assert result.output == "Pylaroid %s\n" % __version__
