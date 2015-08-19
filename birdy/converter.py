#!/usr/bin/env python


from subprocess import call
from . import config

import random
import requests
import urllib.request
import logging


def ID_InterPro(cache):

    logging.info('Fetches InterPro IDs')
    IDs = []

    if cache:
        logging.info('Fetches on InterPro database')
        url = config.url_id_interpro
        file_name = 'ID/InterPro_ID.txt'
        try:
            urllib.request.urlretrieve(url, file_name)
        except urllib.error.URLError:
            logging.error('ftp error with url %s', url)

    with open('ID/InterPro_ID.txt', 'r') as f:
        text = f.read()
    f.closed

    lines = text.split('\n')
    for line in lines:
        IDs.append(line.split(' ')[0])

    IDs = IDs[:-1]
    IDs = IDs[1:]
    logging.info('Fetches InterPro IDs ... ok')

    ## ligne a supprimer !!! ############################################################################################
    IDs = config.INTERPRO_ID
    #####################################################################################################################
    return IDs


def fetch(number, maximum, IDs, path):

    logging.info('Fetches data on InterPro databases')

    files_name = []
    filesf_name = []
    rand_list = random.sample(list(range(len(IDs))), number)

    for n in range(number):
        ID = IDs[rand_list[n]]
        logging.info('**********{0}'.format(ID))
        url = config.url_data_interpro.format(ID)
        r = requests.get(url)
        fastas = r.text
        output = fastas.split('>')
        writting_f = ''
        filefamily_name = config.IPR_name.format(path=path, ID=ID, indice="_align", fmt='fasta')
        file_name = config.IPR_name.format(path=path, ID=ID, indice="", fmt='fasta')
        filesf_name.append(filefamily_name)
        files_name.append(file_name)
        logging.info('number of gene in the family{0} : {1}'.format(ID, len(output)))
        logging.info('Write in file {0}'.format(file_name))
        writting = '>' + output[1]
        with open(file_name, 'w') as f:
            f.write(writting)
        f.closed

        output_len = len(output) - 3

        if output_len < maximum:
            maximum = output_len

        for m in range(maximum):
            i = m + 1
            writting_output = '>' + output[i]
            writting_f = writting_f + writting_output 

        logging.info('Write in file {0}'.format(filefamily_name))
        with open(filefamily_name, 'w') as ff:
            ff.write(writting_f)
        ff.closed
        logging.info('Family {0} ... ok'.format(ID))

    logging.info('Fetches data on InterPro databases ... ok')
    return files_name, filesf_name


def convert(formats, fmts, filename, suffix):
    for fmt in formats:
        if fmt in fmts:
            logging.info('Convertion of {0} in {1} format'.format(filename, fmt))            
            extension = '.' + fmt.lower()
            logging.debug(extension)
            output = filename.replace(suffix, extension)
            logging.debug(output)
            logging.info(
                'Converts {0} in {1} format and write in {2}'.format(filename, fmt, output))
            command = 'squizz -c ' + fmt + ' ' + filename + ' > ' + output
            logging.debug(command)
            call(command, shell=True)
            logging.info('Convertion of {0} in {1} format ... ok'.format(filename, fmt))
    logging.info('Convertion of {0} ... ok'.format(filename))


def clustal_align(filename):
    logging.info('Alignment of {0}'.format(filename))
    command = './clustalw2 ' + filename
    try:
        call(command, shell=True)
        filename_align = filename.replace('.fasta', '.aln')
        logging.info('Alignment of {0} ... ok'.format(filename))
    except not found:
        logging.error('Alignment failed')
        filename_align = filename

    return filename_align

def main(path, cache):
    family_number = config.family_file_nb
    nb_align = config.nb_align
    formats = config.formats_converter
    count = True
    
    fmt_seq = [
        'CODATA', 'EMBL', 'GCG', 'GDE', 'GENBANK', 'IG',
        'NBRF', 'RAW', 'SWISSPROT']
    fmt_align = [
        'FASTA', 'MEGA', 'MSF', 'NEXUS', 'PHYLIP', 'STOCKHOLM']

    logging.info('Data loading')
    #ID = ID_InterPro(cache)
    #file_name = fetch(family_number, nb_align, ID, path)

    ############################################################""
    filesf_name = []
    files_name = []
    IDs = [
        'IPR002351', 'IPR002366', 'IPR002369', 'IPR023418', 'IPR002404',
        'IPR002420', 'IPR031145', 'IPR023266', 'IPR002363', 'IPR016271']
    for ID in IDs:
        filefamily_name = config.IPR_name.format(path=path, ID=ID, indice="_align", fmt='fasta')
        file_nameseq = config.IPR_name.format(path=path, ID=ID, indice="", fmt='fasta')
        filesf_name.append(filefamily_name)
        files_name.append(file_nameseq)

    file_name = [files_name, filesf_name]
    ##########################################################################################

    logging.info('Data loading ... ok\n')
    
    logging.info('Sequence convertion')
    for file_name_seq in file_name[0]:
        suffix = '.fasta'
        convert(formats, fmt_seq, file_name_seq, suffix)
        count = False
    logging.info('Sequence convertion ... ok\n')

    logging.info('Alignment convertion')
    for file_name_align in file_name[1]:
        suffix = '.aln'
        align_file = clustal_align(file_name_align)
        convert(formats, fmt_align, align_file, suffix)
        count = False
    logging.info('Alignment convertion ... ok\n')

    # Error messages
    if count:
        message = ('Hoho, no message =(')
        logging.error(message)


if __name__ == "__main__":
    # execute only if run as a script
    main()
