# search:
# Allowed values: any key words.
search = 'gene'

# file_per_format:
# Allowed values: integer between 1 and 99.
file_per_format = 10

# db_NCBI:
# Allowed values: 'protein', 'nucleotide', 'nuccore', 'nucgss', 'homologene',
# 'popset', 'nucest', 'sequences', 'snp'
db_NCBI = ['nucleotide']

# db_KEGG:
# Allowed values: 'pathway', 'brite', 'module', 'ko', 'genome', 'compound',
# 'glycan', 'reaction', 'rpair', 'rclass', 'enzyme', 'disease', 'drug',
# 'dgroup', 'environ', 'organism'.
db_KEGG = ['pathway']

# nb_align:
# Allowed values: integer between 1 and 50.
nb_align = 10

# family_file_nb:
# Allowed values: integer between 1 and 50.
family_file_nb = file_per_format

# pathway:
path = 'Result/'

# dataset:
# defined the directory to load files.
# If the directory already exist, it will be completed
# /!\, dataset can't contain '.fasta'
dataset = 'dataset_time'

# log file :
log_name = 'birdy.log'

# URL
# PDB:
url_id_pdb = 'http://www.rcsb.org/pdb/rest/customReport.csv?pdbids=*&customReportColumns=structureId&format=csv&service=wsfile'
url_data_pdb = 'ftp://ftp.ebi.ac.uk/pub/databases/rcsb/pdb-remediated/data/structures/divided/{fmt}/{code}/{end}'

# KEGG
url_kegg = 'http://rest.kegg.jp/{type}/{data}'

# DSSP
url_data_dssp = 'ftp://ftp.cmbi.ru.nl/pub/molbio/data/dssp/{0}.dssp'

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


# a remplacer par EDAM

formats_converter = [
    'CODATA', 'EMBL', 'GCG', 'GDE', 'GENBANK', 'IG', 'NBRF', 'RAW',
    'SWISSPROT', 'CLUSTAL', 'MEGA', 'MSF', 'NEXUS', 'PHYLIP', 'STOCKHOLM']
formats_fetcher = ['pdb', 'mmCIF', 'fasta', 'gb', 'gp', 'keg', 'dssp']



#ID test :
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



