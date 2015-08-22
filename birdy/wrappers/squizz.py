import logging
import os.path
import subprocess
import sys

from .. import config
from ..exceptions import UnsupportedFormatError


def squizz(input_filename, input_format, output_format):
    """A simple wrapper for squizz

    Args:
        input_filename: input file
        input_format: input file format
        output_format: output file format

    Returns:
        the output file path
    """
    logging.info(
        "Will convert {input_filename} from {input_format} "
        "to {output_format}".format(
            input_filename=input_filename,
            input_format=input_format,
            output_format=output_format
        )
    )

    io_formats = [input_format, output_format]
    if any(fmt not in config.SQUIZZ_FORMATS for fmt in io_formats):
        msg = "(in|out)put format is not yet supported by squizz"
        logging.error(msg)
        raise UnsupportedFormatError(msg)

    base, ext = os.path.splitext(input_filename)
    log_filename = '{base}.{ext}'.format(base=base, ext='log')
    output_filename = '{base}.{ext}'.format(
        base=base, ext=output_format.lower()
    )

    cmd = (
        '{squizz} -f {input_format} -c {output_format} '
        '{input_filename}'.format(
            squizz=config.SQUIZZ,
            input_format=input_format,
            output_format=output_format,
            input_filename=input_filename
        )
    )

    try:
        with open(log_filename, "w") as log_file, \
             open(output_filename, "w") as output_file:
            subprocess.call(
                cmd,
                stdout=output_file,
                stderr=log_file,
                shell=True
            )
    except:
        logging.error('Squizz conversion failed. Command was: {}'.format(cmd))
        logging.debug(sys.exc_info()[0])
        raise

    if not os.path.exists(output_filename):
        logging.error(
            'Squizz conversion failed. Please check execution log file.'
        )
        return None

    return output_filename
