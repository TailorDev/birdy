import random
import requests
import urllib.request
import logging

from .. import config


def id_PDB(cache):
    """Fetches PDB IDs.

    Retrieves all IDs from PDB data base.

    Args:
        cache : boulean, if True, reloads all IDs, if False,
            use IDs in file "PDB_ID.txt"

    Returns:
        A list of all IDs.
        For exemple :

        ['4Z1S', '4Z1X', '4Z1Y', '4Z24', '4Z25', '4Z26',
         '4Z28', '4Z29', '4Z2B', '4Z2F', '4Z2G', '4Z2H',
         '4Z2I', '4Z2J', '4Z2K', '4Z2L', '4Z2O', '4Z2P']
    """

    logging.info('Fetches PDB IDs')

    if cache:
        logging.info('Fetches PDB IDs on PDB Database')
        url = config.url_id_pdb
        r = requests.get(url)
        IDs = r.text.split('"\n"')
        IDs[0] = IDs[0].split('"')
        IDs[0] = IDs[0][1]
        IDs[-1] = IDs[-1].split('"')
        IDs[-1] = IDs[-1][0]

        if IDs != []:
            logging.info('Writes in PDB_ID.txt file')
            with open('ID/PDB_ID.txt', 'w') as f:
                for ID in IDs:
                    output = ID + '\t'
                    f.write(output)
            f.closed
            logging.info('Writes ok')
        else:
            logging.warning('Problem with PDB database')
            with open('ID/PDB_ID.txt', 'r') as f:
                ID = f.read()
                IDs = ID.split('\t')
            f.closed
            IDs = IDs[:-1]
        logging.info('Fetches on database ok')

    else:
        logging.info('Reads on PDB_ID.txt file')
        with open('ID/PDB_ID.txt', 'r') as f:
            ID = f.read()
            IDs = ID.split('\t')
        f.closed
        IDs = IDs[:-1]

    logging.info('Fetches ok')

    # ligne a supprimer !!! ###############################################
    # IDs = config.PDB_ID
    #######################################################################
    return IDs


def fetch_PDB(IDs, file_per_format, path, fmt, end, extension):
    """Fetches datas about random IDs

    Retrieves datas about a random list of n IDs, in pdb or mmCIF formats,
    in PDB data bases and load it in "path" directory. "n" is
    the number of files per formats
    --- /!\ gzipped format /!\ ---

    Args:
        IDs : IDs list
        file_per_format : number of files per formats
        path : pathway where data will be load
        fmt : pdb or mmCIF formats, used in url
        end : extension for url
    """

    logging.info('Fetches PDB datas about IDs on pdb format')
    rand_list = random.sample(list(range(len(IDs))), file_per_format)

    for i in range(file_per_format):
        ID = IDs[rand_list[i]]
        ID = ID.lower()
        code = ID[:-1]
        code = code[1:]
        final_end = end.format(ID, extension)
        url = config.url_data_pdb.format(fmt=fmt, code=code, end=final_end)
        file_name = config.PDB_name.format(
            path=path, ID=ID, extension=extension)
        try:
            urllib.request.urlretrieve(url, file_name)
            logging.info('{0} ... ok'.format(ID))
        except urllib.error.URLError:
            logging.error('ftp error with url {0} on PDB database'.format(url))


def run_PDB(file_per_format, formats, cache, path):
    """Result

    Manages fonctions about PDB database

    Args:
        file_per_format : number of files per formats
        formats : List of formats
    """

    logging.info('PDB database')

    IDs = id_PDB(cache)
    count = True

    if 'pdb' in formats:
        fmt = 'pdb'
        end = 'pdb{0}.{1}'
        extension = 'ent.gz'
        fetch_PDB(IDs, file_per_format, path, fmt, end, extension)
        logging.info('pdb format ... ok')
        count = False

    if 'mmCIF' in formats:
        fmt = 'mmCIF'
        end = '{0}.{1}'
        extension = 'cif.gz'
        fetch_PDB(IDs, file_per_format, path, fmt, end, extension)
        logging.info('mmCIF format ... ok')
        count = False

    # Error messages
    if count:
        logging.info('No pdb or mmCIF formats load')

    logging.info('PDB database ... ok\n')
