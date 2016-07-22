import logging
import os
import os.path
import requests
import xmltodict

from gzip import GzipFile
from six.moves.urllib import request

from .. import config
from ..compat import makedirs
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
        logging.info("Updating interpro ids cache. This may take minutes...")

        # Create cache directory if it does not exists
        makedirs(config.IDS_LIST_CACHE_ROOT, exist_ok=True)

        ids = []

        def select_interpro_entries(path, item):
            """Select interpro families (ID) with:

            * less than config.INTERPRO_MAX_PROTEIN_COUNT
            """
            # global ids  # this is ugly

            # not an interpro entity
            if 'interpro' not in path[-1]:
                # We return True to avoid stopping gzipped xml stream parsing
                return True

            ipro = path[-1][1]
            if int(ipro['protein_count']) <= config.INTERPRO_MAX_PROTEIN_COUNT:
                ids.append(ipro['id'])

            return True

        # Attention, tricky part
        # We stream ftp response in a GzipFile that is streamed by xmltodict
        with request.urlopen(config.INTERPRO_IDS_URL) as f:
            xmltodict.parse(
                GzipFile(fileobj=f),
                item_depth=2,
                item_callback=select_interpro_entries
            )

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

    makedirs(output_path, exist_ok=True)

    url = config.INTERPRO_ID_URL.format(id=ID, fmt=fmt)

    response = requests.get(url)
    if not response.status_code == 200:
        msg = "An error occured while fetching interpro entry"
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
            try:
                output_file = fetch_interpro(ipro_id, output_path=output_path)
            except NetworkError:
                continue
            output_files += [output_file]
        logging.info("{} files have been fetched".format(len(output_files)))

    logging.info(
        "Interpro | Execution time was {time:.3f} s".format(time=t.secs)
    )

    return output_files
