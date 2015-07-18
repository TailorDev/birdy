#!/usr/bin/python


from Bio_Eutils import Entrez
import random


def conversion(file_per_format, formats_list):
    """
    Fonction permettant de calculer le nombre d'IDs
    à requeter et définitions d'un ordre aléatoire
    file_per_format : Nombre de fichier voulu par type de format
    formats_list : liste des diférent formats voulu
    return : le nombre de fichier total ainsi qu'un ordre aléatoire
    """
    nb_file = file_per_format * len(formats_list)
    liste = list(range(nb_file))
    rand_list = random.sample(liste, nb_file)
    return rand_list, nb_file


def search_db(nb_file, data_base, terms, mail):
    """
    Fonction permettant de requeter dans les base de donnée et
    d'extraire une liste d'IDs
    nb_file : nombre d'IDs requeter
    data_base : base de données dans laquel est faite la requete
    terms : termes de la requete
    mail : mail de l'utilisateur, necessaire pour requeter sur NCBI via Entrez
    return : list d'IDs
    """
    Entrez.email = mail
    handle = Entrez.esearch(db=data_base, retmax=nb_file, term=terms)
    pub_search = Entrez.read(handle)
    handle.close()
    return pub_search['IdList']


def fetch_db(data_base, id_list, formats_list, file_per_format, rand_list):
    """
    requete sur les IDs et extrait les fichiers correspondante sur NCBI
    et les enregistre dans le repertoire "Result" du repertoire courrant
    data_base : base de données de la requete
    id_list : liste d'IDs sur lesquelles sont faite la requete.
    formats_list : liste des diférent formats voulu
    file_per_format : nombre de fichier voulu par format
    rand_list : ordre aléatoire
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
        formats_list, terms, mail,
        file_per_format=10, data_base="nucleotide"):
    result_conversion = conversion(file_per_format, formats_list)
    id_list = search_db(
        result_conversion[1],
        data_base, terms, mail)
    fetch_db(
        data_base, id_list,
        formats_list, file_per_format,
        result_conversion[0])


if __name__ == "__main__":
    # Settings
    formats_list = ["gb", "fasta"]
    file_per_format = 10
    terms = "matK[Gene]"  # Exemple : "Cypripedioideae[Orgn] AND matK[Gene]"
    data_base = "nucleotide"
    mail = "loiseauc48@gmail.com"
    # execute only if run as a script
    result(formats_list, terms, mail, file_per_format, data_base)
