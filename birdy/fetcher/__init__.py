from .. import config
from .pdb import generate_pdb_set
from .ncbi import generate_ncbi_set


def main(output_path, formats=None, use_cache=True):
    # formats = config.formats_fetcher
    # search = config.search
    # file_per_format = config.file_per_format
    # db_NCBI = config.db_NCBI
    # db_KEGG = config.db_KEGG

    if 'PDB' in formats:
        generate_pdb_set(
            output_path,
            formats.get('PDB', None),
            input_ids=None,
            use_cache=use_cache
        )
    if 'NCBI' in formats:
        for db in config.NCBI_DATABASES:
            generate_ncbi_set(
                output_path,
                db,
                formats.get('NCBI', None),
                input_ids=None,
                use_cache=use_cache
            )
    #     run_NCBI(formats, search, file_per_format, db_NCBI, output_path)
    # if 'keg' in formats:
    #     run_KEGG(db_KEGG, file_per_format, use_cache, output_path)
    # if 'dssp' in formats:
    #     run_DSSP(file_per_format, output_path)
