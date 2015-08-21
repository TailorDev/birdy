import logging
import os.path
import sys
import urllib.request

from .. import config
from .pdb import get_random_pdb_ids_set


def fetch_dssp(ID, output_path='.'):
    """Fetch a DSSP file from pdb.org IDs

    Args:
        ID: PDB ID
        output_path: path to output downloaded files
    """

    logging.info('Fetching DSSP {}...'.format(ID))

    fmt = 'dssp'
    filename = '{id}.dssp'.format(id=ID)

    fmt_path = os.path.join(output_path, fmt)
    output_file = os.path.join(fmt_path, filename)

    os.makedirs(fmt_path, exist_ok=True)

    url = config.DSSP_ID_URL.format(id=ID)

    try:
        urllib.request.urlretrieve(url, output_file)
    except:
        logging.error(
            "Cannot fetch id {id} from the CMBI. "
            "Request url was: {url}".format(
                id=ID, url=url
            )
        )
        logging.debug(sys.exc_info()[0])
        raise


def generate_dssp_set(output_path, formats, input_ids=None, use_cache=True):
    """Generate PDB files sample

    Args:
        output_path: the output path
        formats: a dict of format/counter {'fmt': 10}
        IDs: we are able to force PDB/DSSP IDs to download
        use_cache: if False PDB ids list cache will be updated
    """

    logging.info('Handling DSSP file format...')

    fmt = 'dssp'
    if input_ids is None:
        ids = get_random_pdb_ids_set(formats[fmt], use_cache=use_cache)
    else:
        ids = input_ids

    i = 0
    for i, pdb_id in enumerate(ids):
        fetch_dssp(pdb_id, output_path=output_path)
    if i:
        logging.info("{} {} files have been fetched".format(i + 1, fmt))

    logging.info('DSSP file format done\n')
