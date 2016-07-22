import pytest
import subprocess

from os import environ


@pytest.fixture
def entrez():
    environ['ENTREZ_EMAIL'] = 'foo@bar.com'
    return


@pytest.fixture
def run():
    def do_run(args):
        args = ["birdy"] + args
        return subprocess.call(args)
    return do_run


def test_fasta(entrez, tmpdir, run):
    args = ['--fasta', '1', tmpdir.strpath]
    assert run(args) == 0
