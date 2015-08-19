import random
import requests
import logging

from .. import config


def id_KEGG(db, cache):
    """Fetches KEGG IDs.

    Retrieves all IDs from specified KEGG data base like 'pathway'.

    Args:
        db : KEGG database
        cache : boulean, if True, reloads all IDs, if False,
            use IDs in file "KEGG_(database)_ID.txt"

    Returns:
        A list of IDs corresponding on the databases.
        For exemple :

        ['path:map00072', 'path:map00073', 'path:map00100', 'path:map00120',
         'path:map00121', 'path:map00130', 'path:map00140', 'path:map00190',
         'path:map00195', 'path:map00196', 'path:map00220', 'path:map00230',
         'path:map00231', 'path:map00232', 'path:map00240', 'path:map00250']

    """
    logging.info('Fetches KEGG IDs')

    file_name = 'ID/KEGG_' + db + '_ID.txt'

    if cache:
        logging.info('Fetches KEGG IDs on %s database', db)
        url = config.url_kegg.format(type='list', data=db)
        logging.debug(url)
        r = requests.get(url)

        IDs = []
        lines = r.text.split('\n')
        logging.debug(lines)
        for line in lines:
            ID = line.split('\t')

            if ID[0] != '':
                IDs.append(ID[0])
        if IDs != []:
            with open(file_name, 'w') as f:
                for ID in IDs:
                    output = ID + '\t'
                    f.write(output)
            f.closed
        else:
            logging.warning('Problem with KEGG databases')
            with open(file_name, 'r') as f:
                ID = f.read()
                IDs = ID.split('\t')
            f.closed
            IDs = IDs[:-1]

        logging.info('Fetches on database ok')
    else:
        logging.info('Reads on {0} file'.format(file_name))
        with open(file_name, 'r') as f:
            ID = f.read()
            IDs = ID.split('\t')
        f.closed
        IDs = IDs[:-1]
        logging.info('Reads ok')

    logging.info('Fetches ok')

    # ligne a supprimer !!! ################################################
    # IDs = config.KEGG_ID
    ########################################################################
    return IDs


def fetch_KEGG(IDs, file_per_format, path, db):
    """Fetches datas about random IDs

    Retrieves datas about a random list of n IDs, in KEGG data
    bases and load it in "Result/dataset" directory. "n" is the number
    of files per formats

    Args:
        IDs : IDs list
        file_per_format : number of files per formats
    """

    logging.info('Fetches KEGG datas about IDs')

    rand_list = random.sample(list(range(len(IDs))), file_per_format)

    for i in range(file_per_format):
        ID = IDs[rand_list[i]]
        url = config.url_kegg.format(type='get', data=ID)
        r = requests.get(url)
        output = r.text
        file_name = config.KEGG_name.format(path=path, ID=ID)
        with open(file_name, 'w') as f:
            f.write(output)
        f.closed
        logging.info('{0} ... ok'.format(ID))


def run_KEGG(databases, file_per_format, cache, path):
    """Result

    Checks databases and manages fonctions about KEGG database

    Args:
        file_per_format : number of files per formats
        databases : NCBI data base
    """

    logging.info('KEGG database')

    Kdb = [
        'pathway', 'brite', 'module', 'ko', 'genome', 'compound', 'glycan',
        'reaction', 'rpair', 'rclass', 'enzyme', 'disease', 'drug', 'dgroup',
        'environ', 'organism']

    for database in databases:
        if database in Kdb:
            ID = id_KEGG(database, cache)
            fetch_KEGG(ID, file_per_format, path, database)
        # Error messages
        else:
            logging.error(
                'Databases %s not alowed. Try with "pathway", "brite",' +
                ' "module", "ko", "genome", "compound", "glycan", ' +
                ' "reaction", "rpair", "rclass", "enzyme", "disease", ' +
                ' "drug", "dgroup", "environ" or "organism"', database)
    logging.info('KEGG database ... ok\n')
