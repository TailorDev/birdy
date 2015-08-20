import random


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
