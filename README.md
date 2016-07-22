# Birdy

A biological file formats compilation tool.

## Dependencies

Birdy uses third-party tools to convert or generate some file formats. Please,
consider installing them first:

* clustalw: http://www.clustal.org/clustal2/
* squizz: ftp://ftp.pasteur.fr/pub/gensoft/projects/squizz/

Once installed, please check that binaries are available in your path:

```
$ which clustalw2
/usr/local/bin/clustalw2
$ which squizz
/usr/local/bin/squizz
```

If the `which` command returns nothing, you'll need to fix your installation.

## Installation

Clone the repository:

```
$ git clone git@github.com:TailorDev/birdy.git
```

Create a new virtual environment:

```
$ cd birdy
$ pyvenv venv
$ source venv/bin/activate
```

Install `birdy` in your new virtual environment:

```
(venv) $ python setup.py install
```

## Development

If you want to contribute to `birdy`, you will need to install testing
dependencies:

```
$ pip install -r requirements-dev.txt
```

## Usage

Due to restriction usage, the NCBI needs an email address to contact you in case
of troubles. Hence, you'll need to define the `ENTREZ_EMAIL` environment
variable to fetch data from their server:

```
$ export ENTREZ_EMAIL='you@foo.com'
```

Replace `you@foo.com` by you real email address (thank you
[captain obvious](http://giphy.com/gifs/xT9DPCzYKPhe9bWQCY)).

`birdy` command line usage is available via:

```
(venv) $ birdy -h
Usage:
  birdy [options] <output-path>

Options:
  -h  --help     Show this screen.
  -v  --verbose  Verbose mode
  -d  --debug    Debug mode
  -n  --no-cache Do not use cache at all
  --all <num>    Collect num files for all supported file formats

Formats:
  --clustal <num>  Fetch num clustals
  --dssp <num>  Fetch num dssps
  --fasta <num>  Fetch num fastas
  --gb <num>  Fetch num gbs
  --gp <num>  Fetch num gps
  --kegg <num>  Fetch num keggs
  --mmCIF <num>  Fetch num mmCIFs
  --msf <num>  Fetch num msfs
  --nexus <num>  Fetch num nexuss
  --pdb <num>  Fetch num pdbs
  --phylip <num>  Fetch num phylips
```

## Example

As an example, let's say you want a small dataset of 5 fasta files. All you need
is to:

```
(venv) $ birdy --fasta 5 dataset
```

Once done, check that `birdy` has properly downloaded required files via:

```
(venv) $ tree dataset
dataset
└── fasta
    ├── nucleotide
    │   ├── 1043401244.fasta
    │   ├── 1043401273.fasta
    │   ├── 1043401275.fasta
    │   ├── 1043401298.fasta
    │   └── 1043401300.fasta
    └── protein
        ├── 1043520754.fasta
        ├── 1043520761.fasta
        ├── 1043520762.fasta
        ├── 1043520777.fasta
        └── 1043520788.fasta

3 directories, 10 files
```

## License

Birdy is released under the MIT License. See the bundled LICENSE file for
details.
