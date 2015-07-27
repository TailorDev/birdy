#!/usr/bin/python

doc = """Fetcher.

Usage:
  fetcher.py -s <search> [-d <db>] [-F <format>...] [-n <nb>]
  fetcher.py (-h | --help)

Examples:
  fetcher.py -d nucleotide -F gb -F fasta -s matK -n 10

Options:
  -h --help        Show this screen.
  -d=<db>          data base [default: nucleotide]
  -F=<format>      File format [default: fasta].
  -s=<search>      Search term.
  -n=<nb>          File(s) per format [default: 10].

"""

from docopt import docopt
from Bio_Eutils import Entrez
from schema import Schema, And, Or, Use, SchemaError, Optional
import random
import os


Entrez.email = 'loiseauc48@gmail.com'


def search_db(db, search, file_per_format, formats):
    """Fetches IDs.

    Retrieves IDs from specified NCBI data base like 'nucleotide', and
    -a long description-

    Args:
        db : NCBI data base
        search : keyword
        file_per_format : number of file per formats
        formats : List of formats

    Returns:
        A list of IDs corresponding on the 'search' keywards.
        For exemple :

        ['894216361', '894216359', '894216357', '894216355',
        '894216353', '894216351', '894216349', '894216348',
        '894216347', '894216346']
    """

    nb_file = file_per_format * (len(formats))
    i = random.randint(1, 100)

    handle = Entrez.esearch(db=db, retmax=nb_file, retstart=i, term=search)
    pub_search = Entrez.read(handle)
    handle.close()

    return pub_search['IdList']


def fetch_db(db, IDs, formats, file_per_format):
    """Fetches datas about IDs

    Retrieves datas about IDs in specified formats, in NCBI
    data bases and load it in "Result" directory

    Args:
        db : NCBI data base
        IDs : IDs list
        file_per_format : number of file per formats
        formats : List of formats
    """

    rand_list = random.sample(list(range(len(IDs))), len(IDs))
    i = 0

    # Fetch matching entries
    for fmt in formats:
        extension = '.' + fmt
        for n in range(file_per_format):
            start = rand_list[i]
            handle = Entrez.efetch(
                db=db, id=IDs,
                retmax=1, retstart=start,
                rettype=fmt, retmode="text"
                )
            output = handle.read()
            num = IDs[start]
            file_name = 'Result/Test' + str(num) + extension
            with open(file_name, 'w') as f:
                f.write(output)
            i += 1
            handle.close()


def result(formats, search, file_per_format, db):

    IDs = search_db(db, search, file_per_format, formats)

    fetch_db(db, IDs, formats, file_per_format)


if __name__ == "__main__":
    # execute only if run as a script
    args = docopt(doc)

    schema = Schema({
        '-s': And(str, len),
        Optional('-n'): And(Use(int), lambda n: 1 <= n <= 99),
        Optional('-F'): And(list),
        Optional('--help'): bool,
        Optional('-d'): And(str, Use(str.lower), lambda s: s in (
            'pubmed', 'protein', 'nucleotide', 'nuccore', 'nucgss',
            'nucest', 'structure', 'genome', 'books', 'cancerchromosomes',
            'cdd', 'gap', 'domains', 'gene', 'genomeprj', 'gensat', 'geo',
            'gds', 'homologene', 'journals', 'mesh', 'ncbisearch',
            'nlmcatalog', 'omia', 'omim', 'pmc', 'popset', 'probe',
            'proteinclusters', 'pcassay', 'pccompound', 'pcsubstance',
            'snp', 'taxonomy', 'toolkit', 'unigene', 'unists'))})
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)



    formats = args['-F']
    search = args['-s']
    file_per_format = int(args['-n'])
    db = args['-d']

    result(formats, search, file_per_format, db)
