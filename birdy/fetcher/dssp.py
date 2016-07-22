import logging
import os.path
import sys

from ftplib import FTP
from six.moves.urllib import request

from .. import config
from ..compat import makedirs
from ..utils import get_random_ids, Timer


def get_dssp_ids(use_cache=True):
    """Get dssp IDs

    Retrieves all DSSP files from:
    http://www.cmbi.ru.nl/dssp.html

    Args:
        use_cache: boolean, if False force cache update

    Returns:
        A list of DSSP/PDB IDs.
        For exemple :

        ['4z1s.dssp', '4z1y.dssp', '4z24.dssp', '4z25.dssp',
         '4z28.dssp', '4z2b.dssp', '4z2f.dssp', '4z2g.dssp',
         '4z2i.dssp', '4z2k.dssp', '4z2l.dssp', '4z2o.dssp']
    """

    # Update cache
    if not os.path.exists(config.DSSP_IDS_LIST_CACHE) or use_cache is False:
        logging.info("Updating DSSP ids cache...")

        # Create cache directory if it does not exists
        makedirs(config.IDS_LIST_CACHE_ROOT, exist_ok=True)

        # Fetch ids
        ftp = FTP(config.DSSP_FTP_HOST)
        ftp.login()
        ftp.cwd(config.DSSP_FTP_PATH)
        files = ftp.nlst()
        ids = [f.replace('.dssp', '') for f in files]

        # Update cache file
        with open(config.DSSP_IDS_LIST_CACHE, 'w') as f:
            f.write('\n'.join(ids))
    # Use the cache
    else:
        logging.info("Loading DSSP ids from cache...")

        with open(config.DSSP_IDS_LIST_CACHE, 'r') as f:
            ids = [l.replace('\n', '') for l in f.readlines()]

    return ids


def get_random_dssp_ids_set(count, use_cache=True):
    """Get random DSSP ids set"""

    logging.info('Generating DSSP ids sample')

    return get_random_ids(get_dssp_ids(use_cache), count)


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

    makedirs(fmt_path, exist_ok=True)

    url = config.DSSP_ID_URL.format(id=ID)

    try:
        request.urlretrieve(url, output_file)
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

    with Timer() as t:

        fmt = 'dssp'
        if input_ids is None:
            ids = get_random_dssp_ids_set(formats[fmt], use_cache=use_cache)
        else:
            ids = input_ids

        i = 0
        for i, pdb_id in enumerate(ids):
            fetch_dssp(pdb_id, output_path=output_path)
        if i:
            logging.info("{} {} files have been fetched".format(i + 1, fmt))

    logging.info("DSSP | Execution time was {:.3f} s".format(t.secs))
