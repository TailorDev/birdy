#!/usr/bin/python

"""Fetcher.

Usage:
  fetcher.py [-d <db>] [-F <format>...] [-t <term>] [-n <nb>]
  fetcher.py (-h | --help)

Examples:
  fetcher.py -d nucleotide -F gb -F fasta -t matK -n 10

Options:
  -h --help        Show this screen.
  -d=<db>          data base [default: nucleotide]
  -F=<format>      File format [default: fasta].
  -t=<term>        Search term [default: matk].
  -n=<nb>          File per format [default: 10].

"""

from docopt import docopt
from Bio_Eutils import Entrez
import random

Entrez.email = 'loiseauc48@gmail.com'


def conversion(file_per_format, formats_list):
    """
    Fonction permettant de calculer le nombre d'IDs
    a requeter et definitions d'un ordre aleatoire
    file_per_format : Nombre de fichier voulu par type de format
    formats_list : liste des diferent formats voulu
    return : le nombre de fichier total ainsi qu'un ordre aleatoire
    """
    nb_file = file_per_format * (len(formats_list))
    liste = list(range(nb_file))
    rand_list = random.sample(liste, nb_file)
    return rand_list, nb_file


def search_db(nb_file, data_base, terms):
    """
    Search IDs on NCBI data bases
    nb_file : number of IDs
    data_base : NCBI data base
    terms : keyword
    return : IDs list
    """
    i = random.randint(1, 1000000)
    handle = Entrez.esearch(db=data_base, retmax=nb_file, retstart=i, term=terms)
    pub_search = Entrez.read(handle)
    handle.close()
    return pub_search['IdList']


def fetch_db(data_base, id_list, formats_list, file_per_format, rand_list):
    """
    requete sur les IDs et extrait les fichiers correspondante sur NCBI
    et les enregistre dans le repertoire "Result" du repertoire courrant
    data_base : base de donnees de la requete
    id_list : liste d'IDs sur lesquelles sont faite la requete.
    formats_list : liste des diferent formats voulu
    file_per_format : nombre de fichier voulu par format
    rand_list : ordre aleatoire
    """
    loop = file_per_format
    i = 0
    # Fetch matching entries
    for format_single in formats_list:
        extension = '.' + format_single
        while i < loop:
            start = rand_list[i]
            handle = Entrez.efetch(
                db=data_base, id=id_list,
                retmax=1, retstart=start,
                rettype=format_single, retmode="text"
                )
            output = handle.read()
            num = id_list[start]
            file_name = 'Result/Test' + str(num) + extension
            with open(file_name, 'w') as f:
                f.write(output)
            i += 1
            handle.close()
        loop = loop + file_per_format


def result(
        formats_list, terms="gene",
        file_per_format=10, data_base="nucleotide"):
    result_conversion = conversion(file_per_format, formats_list)
    id_list = search_db(
        result_conversion[1],
        data_base, terms)
    fetch_db(
        data_base, id_list,
        formats_list, file_per_format,
        result_conversion[0])


if __name__ == "__main__":
    # execute only if run as a script
    args = docopt(__doc__)
    result(args['-F'], args['-t'], int(args['-n']), args['-d'])
