import os.path
import pytest

from birdy import compat


def test_makedirs(tmpdir):
    """Test makedirs compatibility layer"""

    new_path = os.path.join(tmpdir.strpath, 'foo', 'bar', 'spam')
    assert not os.path.exists(new_path)

    compat.makedirs(new_path, exist_ok=True)
    assert os.path.exists(new_path)

    # Calling this function two times in a row should not return an exception
    # with exist_ok set to True
    compat.makedirs(new_path, exist_ok=True)
    assert os.path.exists(new_path)

    # Now we don't want to ignore existing directories
    with pytest.raises(OSError) as excinfo:
        compat.makedirs(new_path, exist_ok=False)
    assert excinfo.value.errno == 17
