from .. import config
from .dssp import run_DSSP
from .kegg import run_KEGG
from .ncbi import run_NCBI
from .pdb import generate_pdb_set


def main(output_path, cache):
    formats = config.formats_fetcher
    search = config.search
    file_per_format = config.file_per_format
    db_NCBI = config.db_NCBI
    db_KEGG = config.db_KEGG
    pdb = False
    NCBI = False
    pdbformat = ['pdb', 'mmCIF']
    NCBIformat = ['fasta', 'gb', 'gp']
    for fmt in formats:
        if fmt in pdbformat:
            pdb = True
    for fmt in formats:
        if fmt in NCBIformat:
            NCBI = True
    if pdb:
        generate_pdb_set(
            output_path,
            file_per_format,
            config.FORMATS.get('PDB', None),
            input_ids=None,
            use_cache=cache
        )
    if NCBI:
        run_NCBI(formats, search, file_per_format, db_NCBI, output_path)
    if 'keg' in formats:
        run_KEGG(db_KEGG, file_per_format, cache, output_path)
    if 'dssp' in formats:
        run_DSSP(file_per_format, output_path)
