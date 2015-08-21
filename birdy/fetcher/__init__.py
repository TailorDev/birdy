import logging

from .. import config
from .dssp import generate_dssp_set
from .kegg import generate_kegg_set
from .ncbi import generate_ncbi_set
from .pdb import generate_pdb_set


def main(output_path, formats=None, use_cache=True):

    # PDB
    if sum(formats.get('PDB').values()):

        generate_pdb_set(
            output_path,
            formats.get('PDB'),
            input_ids=None,
            use_cache=use_cache
        )

    # NCBI
    if sum(formats.get('NCBI').values()):

        for db in config.NCBI_DATABASES:

            generate_ncbi_set(
                output_path,
                db,
                formats.get('NCBI'),
                input_ids=None,
                use_cache=use_cache
            )

    # KEGG
    if sum(formats.get('KEGG').values()):

        for db in config.KEGG_DATABASES:

            generate_kegg_set(
                output_path,
                db,
                formats.get('KEGG'),
                input_ids=None,
                use_cache=use_cache
            )

    # DSSP
    if sum(formats.get('DSSP').values()):

        generate_dssp_set(
            output_path,
            formats.get('DSSP'),
            input_ids=None,
            use_cache=use_cache
        )
