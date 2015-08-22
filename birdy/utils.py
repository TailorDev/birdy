import random
import time


def get_random_ids(ids, count=10):
    """Generate a random sample form a list"""

    if count > len(ids):
        raise ValueError(
            'Sample size ({}) is greater than the number if ids ({})'.format(
                count,
                len(ids)
            )
        )
    return random.sample(set(ids), count)


class Timer(object):
    """A simple code block wrapper to measure execution time

    example:
    >>> from birdy.utils import Timer
    >>> import time
    >>> with Timer() as t:
    ...     time.sleep(2)
    ...
    >>> print(t.secs)
    2.0047099590301514
    """

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
