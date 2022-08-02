import os

from click.testing import CliRunner

from structuregraph_helpers.cli import get_hash

from .conftest import _THIS_DIR


def test_cli_get_hash():
    runner = CliRunner()
    result = runner.invoke(get_hash, str(os.path.join(_THIS_DIR, "test_files", "HKUST-1.cif")))
    assert result.exit_code == 0
    assert "decorated_graph_hash" in result.output
