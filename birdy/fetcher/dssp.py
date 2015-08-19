import random
import urllib.request
import logging

from .. import config


def id_DSSP():
    """Fetches DSSP IDs.

    Retrieves all IDs from file "DSSP_ID.txt".

    Returns:
        A list of all IDs.
        For exemple :

        ['1cdt', '1cdu', '1cdw', '1cdy', '1cdz',
         '1ce0', '1ce1', '1ce2', '1ce3', '1ce4',
         '1ce5', '1ce6', '1ce7', '1ce8', '1ce9']
    """
    logging.info('Reads on DSSP_ID.txt file')
    with open('ID/DSSP_ID.txt', 'r') as f:
        ID = f.read()
        IDs = ID.split('\t')
    f.closed
    IDs = IDs[:-1]
    logging.info('Reads ok')
    # ligne a supprimer !!! ###############################################
    # IDs = config.DSSP_ID
    #######################################################################
    return IDs


def fetch_DSSP(IDs, file_per_format, path):
    """Fetches datas about IDs

    Retrieves datas about a random list of n IDs in DSSP data base
    and load it in "Result/dataset" directory. "n" is the number of files
    per formats.

    Args:
        IDs : IDs list
        file_per_format : number of file per formats
    """

    logging.info('Fetches DSSP datas about IDs')

    rand_list = random.sample(list(range(len(IDs))), file_per_format)

    for i in range(file_per_format):
        ID = IDs[rand_list[i]]
        ID = ID.lower()
        url = config.url_data_dssp.format(ID)
        file_name = config.DSSP_name.format(path=path, ID=ID)
        try:
            urllib.request.urlretrieve(url, file_name)
            logging.info('{0} ... ok'.format(ID))
        except urllib.error.URLError:
            logging.error('ftp error with url %s on DSSP database', url)


def run_DSSP(file_per_format, path):
    """Result

    Manages fonctions about DSSP database

    Args:
        file_per_format : number of files per formats

    """
    logging.info('DSSP database')
    IDs = id_DSSP()
    fetch_DSSP(IDs, file_per_format, path)
    logging.info('DSSP database ... ok\n')
