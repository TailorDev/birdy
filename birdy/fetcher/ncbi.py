import logging
import os.path
import random

from Bio_Eutils import Entrez

from .. import config
from ..compat import makedirs
from ..exceptions import ConfigurationError
from ..utils import get_random_ids, Timer


def get_random_ncbi_ids_set(count, db, keyword_search):
    """Get random NCBI ids"""

    logging.info('Fetching {} NCBI IDs for the {} database'.format(count, db))

    if not config.ENTREZ_EMAIL:
        msg = (
            "ENTREZ_EMAIL environnment variable undefined. "
            "You must define one with a valid email to use this program."
        )
        logging.error(msg)
        raise ConfigurationError(msg)

    Entrez.email = config.ENTREZ_EMAIL

    retstart = random.randint(1, 10000)
    retmax = count * 10

    handle = Entrez.esearch(
        db=db, retmax=retmax, retstart=retstart, term=keyword_search
    )
    pub_search = Entrez.read(handle)
    handle.close()

    return get_random_ids(pub_search['IdList'], count)


def fetch_ncbi(ID, db, fmt='fasta', output_path='.'):
    """Fetch a ncbi entity

    Args:
        ID: NCBI ID
        fmt: file format
        output_path: path to output downloaded files
    """

    logging.info('Fetching NCBI ID {} with format {}...'.format(ID, fmt))

    filename = '{id}.{fmt}'.format(id=ID, fmt=fmt)

    db_fmt_path = os.path.join(output_path, fmt, db)
    output_file = os.path.join(db_fmt_path, filename)

    makedirs(db_fmt_path, exist_ok=True)

    handle = Entrez.efetch(db=db, id=ID, rettype=fmt, retmode="text")
    response = handle.read()
    with open(output_file, 'w') as f:
        f.write(response)


def generate_ncbi_set(output_path, db, formats, input_ids, use_cache=True):
    """Generate NCBI files sample

    Args:
        output_path: the output path
        formats: a dict of format/counter {'fmt': 10}
        IDs: we are able to force PDB IDs to download
        use_cache: if False PDB ids list cache will be updated
    """
    logging.info('Handling NCBI compatible file formats...')

    for fmt in formats.keys():

        with Timer() as t:

            if input_ids is None:
                ids = get_random_ncbi_ids_set(
                    formats[fmt], db, config.ENTREZ_SEARCH
                )
            else:
                ids = input_ids

            i = 0
            for i, ncbi_id in enumerate(ids):
                fetch_ncbi(ncbi_id, db, fmt=fmt, output_path=output_path)
            if i:
                logging.info(
                    "{} {} files have been fetched".format(i + 1, fmt)
                )

        logging.info(
            "NCBI:{db}:{fmt} | Execution time was {time:.3f} s".format(
                db=db, fmt=fmt, time=t.secs
            )
        )
