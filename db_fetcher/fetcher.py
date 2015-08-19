#!usr/bin/python


from Bio import Entrez
from . import config

import random
import requests
import urllib.request
import logging


def id_NCBI(db, search, file_per_format, formats):
    """Fetches NCBI IDs.

    Retrieves IDs from specified NCBI data base like 'nucleotide'

    Args:
        db : NCBI data base
        search : keyword
        file_per_format : number of file per formats
        formats : List of formats

    Returns:
        A list of IDs corresponding on the 'search' keywards.
        For exemple :

        ['894216361', '894216359', '894216357', '894216355',
         '894216353', '894216351', '894216349', '894216348']
    """

    logging.info('Fetches NCBI IDs on %s database', db)

    Entrez.email = 'loiseauc48@gmail.com'
    nb_file = file_per_format * (len(formats))
    i = random.randint(1, 1000)

    ########################################################################################################################
    i = 1
    ########################################################################################################################

    handle = Entrez.esearch(db=db, retmax=nb_file, retstart=i, term=search)
    pub_search = Entrez.read(handle)
    handle.close()

    logging.info('Fetches NCBI ok')

    return pub_search['IdList']


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

    ## ligne a supprimer !!! ############################################################################################
    IDs = config.PDB_ID
    #####################################################################################################################
    return IDs


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
    ## ligne a supprimer !!! ############################################################################################
    IDs = config.DSSP_ID
    #####################################################################################################################
    return IDs


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

    ## ligne a supprimer !!! ############################################################################################
    IDs = config.KEGG_ID
    #####################################################################################################################
    return IDs



def fetch_NCBI(db, IDs, formats, file_per_format, path):
    """Fetches datas about IDs

    Retrieves datas about IDs in specified formats in NCBI
    data bases, in random order and load it in "Result/dataset" directory

    Args:
        db : NCBI data base
        IDs : IDs list
        file_per_format : number of file per formats
        formats : List of formats
    """

    logging.info(
        'Fetches NCBI datas about IDs on %s database and %s format(s)',
        db, formats)

    Entrez.email = 'loiseauc48@gmail.com'
    rand_list = random.sample(list(range(len(IDs))), len(IDs))
    i = 0

    # Fetch matching entries
    for fmt in formats:
        for n in range(file_per_format):
            start = rand_list[i]
            handle = Entrez.efetch(
                db=db, id=IDs,
                retmax=1, retstart=start,
                rettype=fmt, retmode="text"
                )

            output = handle.read()
            num = IDs[start]
            file_name = config.NCBI_name.format(
                path=path, db=db, ID=str(num), fmt=fmt)
            with open(file_name, 'w') as f:
                f.write(output)
            f.closed
            i += 1
            handle.close()
            logging.info('format {0} range {1} ok'.format(fmt, n))

    logging.info('Fetches NCBI datas ok')


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


def fetch_KEGG(IDs, file_per_format, path,db):
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


def run_NCBI(formats, search, file_per_format, databases, path):
    """Result

    Checks databases and formats and manages fonctions about NCBI database

    Args:
        file_per_format : number of files per formats
        formats : List of formats
        search : keyword
        db : NCBI data base
    """

    logging.info('NCBI database')

    Kdb = [
        'protein', 'nucleotide', 'nuccore', 'nucgss', 'homologene',
        'popset', 'nucest', 'sequences', 'snp']
    dbs = []

    for database in Kdb:
        if database in databases:
            dbs.append(database)

    fmts = ['fasta', 'gp', 'gb']
    form = []
    for fmt in formats:
        if fmt in fmts:
            form.append(fmt)

    if form and dbs:
        for db in dbs:
            IDs = id_NCBI(db, search, file_per_format, form)
            fetch_NCBI(db, IDs, form, file_per_format, path)

    # Error messages
    elif dbs:
        logging.error(
            'Formats %s not alowed. Try with "fasta", "gp", or "gb"',
            formats)
    elif form:
        logging.error(
            'Database %s not alowed. Try with "protein", "nucleotide",' +
            '"nuccore", "nucgss", "homologene", "popset", "nucest",' +
            '"sequences" or "snp"', databases)
    else:
        message = (
            'Formats and databases are not alowed. Expected' +
            'formats : "fasta", "gp", "gb"; Expected databases :' +
            '"protein", "nucleotide", "nuccore", "nucgss", "homologene",' +
            '"popset", "nucest", "sequences", "snp"')
        logging.error(message)

    logging.info('NCBI database ... ok\n')


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
                ' "module", "ko", "genome", "compound", "glycan", "reaction",' +
                ' "rpair", "rclass", "enzyme", "disease", "drug", "dgroup",' +
                ' "environ" or "organism"', database)
    logging.info('KEGG database ... ok\n')


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


def main(path, cache):
    formats = config.formats_fetcher
    search = config.search
    file_per_format = config.file_per_format
    db_NCBI = config.db_NCBI
    db_KEGG = config.db_KEGG
    pdb = False
    NCBI = False
    pdbformat = ['pdb', 'mmCIF']
    NCBIformat = ['fasta', 'gb', 'gp']
    for fmt in formats:
        if fmt in pdbformat:
            pdb = True
    for fmt in formats:
        if fmt in NCBIformat:
            NCBI = True
    if pdb:
        run_PDB(file_per_format, formats, cache, path)
    if NCBI:
        run_NCBI(formats, search, file_per_format, db_NCBI, path)
    if 'keg' in formats:
        run_KEGG(db_KEGG, file_per_format, cache, path)
    if 'dssp' in formats:
        run_DSSP(file_per_format, path)


if __name__ == "__main__":
    # execute only if run as a script
    main()
