import os
import os.path

from itertools import chain
from urllib.parse import urljoin


# Entrez
ENTREZ_SEARCH = 'gene'
ENTREZ_EMAIL = os.environ.get('ENTREZ_EMAIL', None)
ENTREZ_DATABASES = [
    'protein', 'nucleotide', 'nuccore', 'nucgss', 'homologene',
    'popset', 'nucest', 'sequences', 'snp'
]

# NCBI databases that will be queried
NCBI_DATABASES = [
    'protein', 'nucleotide'
]

# Allowed values are listed here:
# http://www.kegg.jp/kegg/rest/keggapi.html
KEGG_DATABASES = ['pathway']

# nb_align:
# Allowed values: integer between 1 and 50.
nb_align = 10

# family_file_nb:
# Allowed values: integer between 1 and 50.
# family_file_nb = file_per_format


OUTPUT_PATH = ''

# dataset:
# defined the directory to load files.
# If the directory already exist, it will be completed
# /!\, dataset can't contain '.fasta'
dataset = 'dataset_time'

# log file :
log_name = 'birdy.log'

# Cache
CACHE_ROOT = os.path.join(os.path.expanduser('~'), '.birdy/cache')
IDS_LIST_CACHE_ROOT = os.path.join(CACHE_ROOT, 'ids')
DSSP_IDS_LIST_CACHE = os.path.join(IDS_LIST_CACHE_ROOT, 'dssp')
PDB_IDS_LIST_CACHE = os.path.join(IDS_LIST_CACHE_ROOT, 'pdb')
INTERPRO_IDS_LIST_CACHE = os.path.join(IDS_LIST_CACHE_ROOT, 'interpro')
KEGG_IDS_LIST_CACHE_ROOT = os.path.join(IDS_LIST_CACHE_ROOT, 'kegg')
KEGG_IDS_LIST_CACHE_FOR_DB = KEGG_IDS_LIST_CACHE_ROOT + '/{db}'

# URL
# PDB:
PDB_IDS_URL = 'http://www.rcsb.org/pdb/rest/customReport.csv?pdbids=*&customReportColumns=structureId&format=csv&service=wsfile'  # NOPEP8
PDB_ID_URL = 'ftp://ftp.ebi.ac.uk/pub/databases/rcsb/pdb-remediated/data/structures/divided/{fmt}/{idx}/{filename}'  # NOPEP8

# KEGG
KEGG_API_URL = 'http://rest.kegg.jp/{operation}/{argument}'

# DSSP
DSSP_FTP_HOST = 'ftp.cmbi.ru.nl'
DSSP_FTP_PATH = '/pub/molbio/data/dssp/'
DSSP_ID_URL = 'ftp://' + DSSP_FTP_HOST + DSSP_FTP_PATH + '{id}.dssp'

# InterProScan
url_data_interpro = 'http://www.ebi.ac.uk/interpro/entry/{0}/proteins-matched\
?export=fasta'
url_id_interpro = 'ftp://ftp.ebi.ac.uk/pub/databases/interpro/Current/entry.l\
ist'

# File name
PDB_name = "{path}PDB_{ID}.{extension}.gz"
NCBI_name = "{path}NCBI_{db}_{ID}.{fmt}"
DSSP_name = "{path}DSSP_{ID}.dssp"
KEGG_name = "{path}KEGG_{ID}.keg"
IPR_name = "{path}INTERPRO_{ID}{indice}.{fmt}"

# A remplacer par EDAM
formats_converter = [
    'CODATA', 'EMBL', 'GCG', 'GDE', 'GENBANK', 'IG', 'NBRF', 'RAW',
    'SWISSPROT', 'CLUSTAL', 'MEGA', 'MSF', 'NEXUS', 'PHYLIP', 'STOCKHOLM']
formats_fetcher = ['pdb', 'mmCIF', 'fasta', 'gb', 'gp', 'keg', 'dssp']
FORMATS = {
    # Service
    'PDB': {
        # Format
        'pdb': 0,
        'mmCIF': 0
    },
    'NCBI': {
        'fasta': 0,
        'gb': 0,
        'gp': 0
    },
    'KEGG': {
        'kegg': 0
    },
    'DSSP': {
        'dssp': 0
    }
}
FORMATS_LIST = sorted([v for v in chain.from_iterable(FORMATS.values())])

# ID test
KEGG_ID = [
    'path:map00909', 'path:map00910', 'path:map00920', 'path:map00930',
    'path:map00940', 'path:map00941', 'path:map00942', 'path:map00943',
    'path:map00944', 'path:map00945']
DSSP_ID = [
    '1a00', '1a01', '1a02', '1a03', '1a04', '1a05', '1a06', '1a07',
    '1a08', '1a09']
INTERPRO_ID = [
    'IPR002351', 'IPR002366', 'IPR002369', 'IPR023418', 'IPR002404',
    'IPR002420', 'IPR031145', 'IPR023266', 'IPR002363', 'IPR016271']
PDB_ID = [
    '175D', '175L', '176D', '176L', '177D', '177L', '178D', '178L',
    '179D', '17GS']
