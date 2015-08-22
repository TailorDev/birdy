import os.path

from .clustal import generate_clustal_set
from .squizz import generate_squizz_set


def main(output_path, formats=None, use_cache=True):

    # Clustal
    if sum(formats.get('CLUSTAL').values()):
        clustal_path = os.path.join(output_path, 'clustal')
        generate_clustal_set(
            clustal_path,
            formats.get('CLUSTAL'),
            input_ids=None,
            use_cache=use_cache
        )

    # Clustal
    if sum(formats.get('SQUIZZ').values()):
        generate_squizz_set(
            output_path,
            formats.get('SQUIZZ'),
            input_ids=None,
            use_cache=use_cache
        )
