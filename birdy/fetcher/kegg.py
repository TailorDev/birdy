import logging
import os.path
import requests

from .. import config
from ..compat import makedirs
from ..exceptions import NetworkError
from ..utils import get_random_ids, Timer


def get_kegg_ids(db, use_cache=True):
    """Fetches KEGG IDs.

    Retrieves all IDs from specified KEGG database, e.g. 'pathway'.

    Args:
        db : KEGG database
        use_cache: boolean, if False force cache update

    Returns:
        A list of IDs corresponding on the databases.
        For exemple :

        ['path:map00072', 'path:map00073', 'path:map00100', 'path:map00120',
         'path:map00121', 'path:map00130', 'path:map00140', 'path:map00190',
         'path:map00195', 'path:map00196', 'path:map00220', 'path:map00230',
         'path:map00231', 'path:map00232', 'path:map00240', 'path:map00250']
    """
    ids_list_cache = config.KEGG_IDS_LIST_CACHE_FOR_DB.format(db=db)

    # Update cache
    if not os.path.exists(ids_list_cache) or use_cache is False:
        logging.info("Updating KEGG ids cache for {} database...".format(db))

        # Create cache directory if it does not exists
        makedirs(config.KEGG_IDS_LIST_CACHE_ROOT, exist_ok=True)

        url = config.KEGG_API_URL.format(
            operation='list', argument=db
        )

        # Fetch PDB ids
        response = requests.get(url)
        if not len(response.text):
            msg = "Got an empty response from rest.kegg.jp"
            logging.error(msg)
            raise NetworkError(msg)
        ids = [l.split('\t')[0] for l in response.text.split('\n') if len(l)]

        # Update cache file
        with open(ids_list_cache, 'w') as f:
            f.write('\n'.join(ids))
    # Use the cache
    else:
        logging.info("Loading KEGG ids from cache...")

        with open(ids_list_cache, 'r') as f:
            ids = [l.replace('\n', '') for l in f.readlines()]

    return ids


def get_random_kegg_ids_set(count, db, use_cache=True):
    """Get random KEGG ids set"""

    logging.info('Generating KEGG ids sample')

    return get_random_ids(get_kegg_ids(db, use_cache), count)


def fetch_kegg(ID, db, output_path='.'):
    """Fetch a KEGG file from kegg.jp rest API

    Args:
        ID: KEGG database entry ID
        db: KEGG database
        output_path: path to output downloaded files
    """
    logging.info('Fetching KEGG {} from database {}...'.format(ID, db))

    fmt = 'kegg'
    filename = '{id}.keg'.format(id=ID)

    db_fmt_path = os.path.join(output_path, fmt, db)
    output_file = os.path.join(db_fmt_path, filename)

    makedirs(db_fmt_path, exist_ok=True)

    url = config.KEGG_API_URL.format(operation='get', argument=ID)

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


def generate_kegg_set(output_path, db, formats, input_ids, use_cache=True):
    """Generate KEGG files sample

    Args:
        output_path: the output path
        formats: a dict of format/counter {'fmt': 10}
        IDs: we are able to force IDs to download
        use_cache: if False ids list cache will be updated
    """
    logging.info('Handling KEGG compatible file formats...')

    for fmt in formats.keys():

        with Timer() as t:

            if input_ids is None:
                ids = get_random_kegg_ids_set(
                    formats[fmt], db, use_cache=use_cache
                )
            else:
                ids = input_ids

            i = 0
            for i, kegg_id in enumerate(ids):
                fetch_kegg(kegg_id, db, output_path=output_path)
            if i:
                logging.info(
                    "{} {} files have been fetched".format(i + 1, fmt)
                )

        logging.info(
            "KEGG:{db}:{fmt} | Execution time was {time:.3f} s".format(
                db=db, fmt=fmt, time=t.secs
            )
        )
