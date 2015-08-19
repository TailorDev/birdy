import random
import logging

from Bio_Eutils import Entrez

from .. import config


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

    #######################################################################
    # i = 1
    #######################################################################

    handle = Entrez.esearch(db=db, retmax=nb_file, retstart=i, term=search)
    pub_search = Entrez.read(handle)
    handle.close()

    logging.info('Fetches NCBI ok')

    return pub_search['IdList']


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
