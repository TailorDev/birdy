import pytest
import subprocess

from os import environ, listdir, path


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
    """Test fasta files fetching from NCBI databases"""

    args = ['--fasta', '1', tmpdir.strpath]
    fasta_dir = path.join(tmpdir.strpath, 'fasta')

    assert run(args) == 0
    assert path.exists(fasta_dir)

    for biotype in ('nucleotide', 'protein'):
        fasta_type_dir = path.join(fasta_dir, biotype)
        assert path.exists(fasta_type_dir)
        fasta_type_files = listdir(fasta_type_dir)
        assert len(fasta_type_files) == 1
        assert fasta_type_files[0][-6:] == '.fasta'
        assert path.getsize(path.join(fasta_type_dir, fasta_type_files[0])) > 0
