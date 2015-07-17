#!/usr/bin/python


from Bio_Eutils import Entrez
import random 
Entrez.email = "loiseauc48@gmail.com"


# Settings
Formats = ["gb","fasta"]
FilePerFormat = 10
Term = "matK[Gene]"   # Exemple : "Cypripedioideae[Orgn] AND matK[Gene]" or "txid158330[Orgn]"
DB = "nucleotide"


NbFile = FilePerFormat * len(Formats)
liste = list(range(NbFile))
RandList = random.sample(liste, NbFile)
Boucle = FilePerFormat
i=0


# Search for IDs 
handle = Entrez.esearch(db=DB, retmax=NbFile, term=Term)
pub_search = Entrez.read(handle)
handle.close()


# Fetch matching entries
for Format in Formats:
	extension = '.'+ Format
	while i<Boucle: 
		Start = RandList[i]
		handle = Entrez.efetch(db=DB, id=pub_search['IdList'], retmax=1, retstart=Start, rettype=Format, retmode="text")
		Dedans = handle.read()
		Num = pub_search['IdList'][Start]
		File = 'Result/Test' + str(Num) + extension
		#with open(File, 'w') as f:
		#	f.write(Dedans)
		print File
		i+=1
		handle.close()
	Boucle = Boucle + FilePerFormat


