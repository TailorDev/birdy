"""
Python2/3 compatibility library
"""
import os


def makedirs(path, exist_ok=False):
    """Compatibility layer for os.makedirs"""
    # Python 3
    try:
        os.makedirs(path, exist_ok=exist_ok)
    except TypeError:
        # Python 2
        try:
            os.makedirs(path)
        except OSError as e:
            # We do not care if the directory already exists
            if e.errno == 17 and exist_ok is True:
                pass
            else:
                raise
