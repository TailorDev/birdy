import logging
import os.path
import subprocess
import sys

from .. import config


def clustalw(filename):
    """A simple wrapper for clustalw2

    Args:
        filename: a multi-fasta file path

    Returns:
        the output alignment filename
    """
    logging.info("Will align {} file with clustalw".format(filename))

    base, ext = os.path.splitext(filename)
    log_filename = '{base}.{ext}'.format(base=base, ext='log')

    cmd = '{bin} {filename}'.format(
        bin=config.CLUSTALW,
        filename=os.path.basename(filename)
    )

    try:
        with open(log_filename, "w+") as log_file:
            subprocess.call(
                cmd, stdout=log_file, shell=True, cwd=os.path.dirname(filename)
            )
    except:
        logging.error('Clustal alignment failed. Command was: {}'.format(cmd))
        logging.debug(sys.exc_info()[0])
        raise

    # Check produced alignment
    align_filename = '{base}.{ext}'.format(
        base=base, ext='aln'
    )
    if not os.path.exists(align_filename):
        logging.error(
            'No alignment was produced. Please check execution log file.'
        )
        return None

    return align_filename
