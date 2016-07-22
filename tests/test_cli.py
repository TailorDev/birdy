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


def _test_format(file_format, tmpdir, run, num=1, biotypes=[], extension=None):

    args = ['--{}'.format(file_format), str(num), tmpdir.strpath]
    format_dir = path.join(tmpdir.strpath, file_format)
    if extension is None:
        extension = '.{}'.format(file_format)

    assert run(args) == 0
    assert path.exists(format_dir)

    def _test_format_type(format_type_dir):
        assert path.exists(format_type_dir)
        format_type_files = [
            f for f in listdir(format_type_dir) if f.endswith(extension)
        ]
        assert len(format_type_files) == num
        assert format_type_files[0].endswith(extension)
        format_type_file = path.join(format_type_dir, format_type_files[0])
        assert path.getsize(format_type_file) > 0

    if not len(biotypes):
        _test_format_type(format_dir)
        return

    for biotype in biotypes:
        format_type_dir = path.join(format_dir, biotype)
        _test_format_type(format_type_dir)


def test_fasta(entrez, tmpdir, run):
    """Test fasta files fetching from NCBI databases"""

    _test_format('fasta', tmpdir, run, num=1, biotypes=('nucleotide', 'protein'))


def test_gb(entrez, tmpdir, run):
    """Test gb files fetching from NCBI databases"""

    _test_format('gb', tmpdir, run, num=1, biotypes=('nucleotide', 'protein'))


def test_gp(entrez, tmpdir, run):
    """Test gp files fetching from NCBI databases"""

    _test_format('gp', tmpdir, run, num=1, biotypes=('nucleotide', 'protein'))
