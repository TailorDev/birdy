import logging

from ..fetcher.interpro import generate_interpro_set
from ..utils import Timer
from ..wrappers.clustalw import clustalw


def generate_clustal_set(output_path, formats, input_ids=None, use_cache=True):
    """Generate Clustal files sample

    In this case, an entire interpro family is downloaded in multi-fasta format
    and is then aligned thanks to clustalw.

    Args:
        output_path: the output path
        formats: a dict of format/counter {'fmt': 10}
        IDs: we are able to force interpro IDs to download
        use_cache: if False interpro ids list cache will be updated
    """

    logging.info('Handling clustal file format...')

    with Timer() as t:

        fmt = 'clustal'
        output_files = generate_interpro_set(
            output_path,
            formats[fmt],
            input_ids=input_ids,
            use_cache=use_cache
        )

        alignements = []
        for ipro in output_files:
            alignements += [clustalw(ipro)]
        logging.info(
            "{} files have been aligned with clustalw".format(len(alignements))
        )

    logging.info("CLUSTAL | Execution time was {:.3f} s".format(t.secs))

    return alignements
