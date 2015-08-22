import logging
import os.path

from ..utils import Timer
from ..wrappers.squizz import squizz
from .clustal import generate_clustal_set


def generate_squizz_set(output_path, formats, input_ids=None, use_cache=True):
    """Generate Squizz compatible files sample

    In this case, an entire interpro family is downloaded in multi-fasta format
    and is then aligned thanks to clustalw. Alignment is then converted with
    squizz.

    Args:
        output_path: the output path
        formats: a dict of format/counter {'fmt': 10}
        IDs: we are able to force interpro IDs to download
        use_cache: if False interpro ids list cache will be updated
    """

    logging.info('Handling squizz compatible file formats...')

    for fmt in formats:

        with Timer() as t:

            fmt_path = os.path.join(output_path, fmt)

            alignments = generate_clustal_set(
                fmt_path,
                {'clustal': formats[fmt]},
                input_ids=input_ids,
                use_cache=use_cache
            )

            converted = []
            for alignment in alignments:
                converted += [squizz(alignment, 'CLUSTAL', fmt.upper())]

        logging.info(
            "SQUIZZ:{fmt} | Execution time was {time:.3f} s".format(
                fmt=fmt, time=t.secs
            )
        )
