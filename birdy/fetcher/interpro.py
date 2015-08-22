import logging
import os
import os.path
import requests
import urllib.request


from .. import config
from ..exceptions import NetworkError
from ..utils import get_random_ids, Timer


def get_interpro_ids(use_cache=True):
    """Get interpro IDs

    Retrieves all IDs from interpro.

    Args:
        use_cache: boolean, if False force cache update

    Returns:
        A list of interpro IDs.
        For exemple :

        ['IPR025875', 'IPR026393', ...]
    """
    # Update cache
    if not os.path.exists(config.INTERPRO_IDS_LIST_CACHE) or \
            use_cache is False:
        logging.info("Updating interpro ids cache...")

        # Create cache directory if it does not exists
        os.makedirs(config.IDS_LIST_CACHE_ROOT, exist_ok=True)

        # Fetch ids
        with urllib.request.urlopen(config.INTERPRO_IDS_URL) as f:
            response = f.read().decode('utf-8')

        if not len(response):
            msg = "Got an empty response from interpro"
            logging.error(msg)
            raise NetworkError(msg)
        ids = [l.split()[0] for l in response.split('\n') if len(l)]

        # Update cache file
        with open(config.INTERPRO_IDS_LIST_CACHE, 'w') as f:
            f.write('\n'.join(ids))
    # Use the cache
    else:
        logging.info("Loading interpro ids from cache...")

        with open(config.INTERPRO_IDS_LIST_CACHE, 'r') as f:
            ids = [l.replace('\n', '') for l in f.readlines()]

    return ids


def get_random_interpro_ids_set(count, use_cache=True):
    """Get random interpro ids set"""

    logging.info('Generating interpro ids sample')

    return get_random_ids(get_interpro_ids(use_cache), count)


def fetch_interpro(ID, fmt='fasta', output_path='.'):
    """Fetch an interpro family fasta file

    Args:
        ID: interpro ID
        fmt: file format
        output_path: path to output downloaded files
    """

    logging.info('Fetching Interpro {}...'.format(ID))

    filename = '{id}.{fmt}'.format(id=ID, fmt=fmt)

    output_file = os.path.join(output_path, filename)

    os.makedirs(output_path, exist_ok=True)

    url = config.INTERPRO_ID_URL.format(id=ID, fmt=fmt)

    response = requests.get(url)
    if not len(response.text):
        msg = (
            "Got an empty response from rest.kegg.jp while fetching kegg "
            "entry"
        )
        logging.error(msg)
        raise NetworkError(msg)

    with open(output_file, 'w') as f:
        f.write(response.text)

    return output_file


def generate_interpro_set(output_path, count, input_ids=None, use_cache=True):
    """Generate PDB files sample

    Args:
        output_path: the output path
        formats: a dict of format/counter {'fmt': 10}
        IDs: we are able to force interpro IDs to download
        use_cache: if False PDB ids list cache will be updated
    """
    logging.info('Generate interpro dataset...')

    output_files = []

    with Timer() as t:

        if input_ids is None:
            ids = get_random_interpro_ids_set(count, use_cache=use_cache)
        else:
            ids = input_ids

        i = 0
        for i, ipro_id in enumerate(ids):
            output_file = fetch_interpro(ipro_id, output_path=output_path)
            output_files += [output_file]
        if i:
            logging.info("{} files have been fetched".format(i + 1))

    logging.info(
        "Interpro | Execution time was {time:.3f} s".format(time=t.secs)
    )

    return output_files
