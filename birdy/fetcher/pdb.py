import logging
import os
import os.path
import requests
import sys
import urllib.request


from .. import config
from ..exceptions import NetworkError, UnsupportedFormatError
from ..utils import get_random_ids


def get_pdb_ids(use_cache=True):
    """Get PDB IDs

    Retrieves all IDs from the PDB.

    Args:
        use_cache: boolean, if False force cache update

    Returns:
        A list of PDB IDs.
        For exemple :

        ['4z1s', '4z1x', '4z1y', '4z24', '4z25', '4z26',
         '4z28', '4z29', '4z2b', '4z2f', '4z2g', '4z2h',
         '4z2i', '4z2j', '4z2k', '4z2l', '4z2o', '4z2p']
    """

    # Update cache
    if not os.path.exists(config.PDB_IDS_LIST_CACHE) or use_cache is False:
        logging.info("Updating PDB ids cache...")

        # Create cache directory if it does not exists
        os.makedirs(config.IDS_LIST_CACHE_ROOT, exist_ok=True)

        # Fetch PDB ids
        response = requests.get(config.PDB_IDS_URL)
        csv = response.text
        if not len(csv):
            msg = "Got an empty response from pdb.org"
            logging.error(msg)
            raise NetworkError(msg)
        ids = [pdb_id.replace('"', '').lower() for pdb_id in csv.split()[1:]]

        # Update cache file
        with open(config.PDB_IDS_LIST_CACHE, 'w') as f:
            f.write('\n'.join(ids))
    # Use the cache
    else:
        logging.info("Loading PDB ids from cache...")

        with open(config.PDB_IDS_LIST_CACHE, 'r') as f:
            ids = [l.replace('\n', '') for l in f.readlines()]

    return ids


def get_random_pdb_ids_set(count, use_cache=True):
    """Get random PDB ids set"""

    logging.info('Generating PDB ids sample')

    return get_random_ids(get_pdb_ids(use_cache), count)


def fetch_pdb(ID, fmt='pdb', output_path='.'):
    """Fetch a PDB file from pdb.org ftp

    Args:
        ID: PDB ID
        fmt: file format
        output_path: path to output downloaded files
    """

    logging.info('Fetching PDB {} with format {}...'.format(ID, fmt))

    if fmt == 'pdb':
        filename = '{id}.ent.gz'.format(id=ID)
    elif fmt == 'mmCIF':
        filename = '{id}.cif.gz'.format(id=ID)
    else:
        msg = "{} format is not yet supported for PDB".format(fmt)
        logging.error(msg)
        raise UnsupportedFormatError(msg)

    fmt_path = os.path.join(output_path, fmt)
    output_file = os.path.join(fmt_path, filename)

    os.makedirs(fmt_path, exist_ok=True)

    url = config.PDB_ID_URL.format(fmt=fmt, idx=ID[1:3], filename=filename)

    try:
        urllib.request.urlretrieve(url, output_file)
    except:
        logging.error(
            "Cannot fetch id {id} from the PDB. Request url was: {url}".format(
                id=ID, url=url
            )
        )
        logging.debug(sys.exc_info()[0])
        raise


def generate_pdb_set(output_path, formats, input_ids=None, use_cache=True):
    """Generate PDB files sample

    Args:
        output_path: the output path
        formats: a dict of format/counter {'fmt': 10}
        IDs: we are able to force PDB IDs to download
        use_cache: if False PDB ids list cache will be updated
    """

    logging.info('Handling PDB file format...')

    for fmt in formats.keys():
        if input_ids is None:
            ids = get_random_pdb_ids_set(formats[fmt], use_cache=use_cache)
        else:
            ids = input_ids

        i = 0
        for i, pdb_id in enumerate(ids):
            fetch_pdb(pdb_id, fmt=fmt, output_path=output_path)
        if i:
            logging.info("{} {} files have been fetched".format(i + 1, fmt))

    logging.info('PDB file format done\n')
