import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))

from private_calls.private_calls_check import main


def test_sad_path():
    expected_exception_msg = "^Violation found @ tests/mock_project/b.py: _fn2 is being called even though it's a private function not defined inside the module.$"
    with pytest.raises(Exception, match=expected_exception_msg):
        main.main("tests/mock_project/a.py", "tests/mock_project/b.py")


def test_happy_path():
    main.main("tests/mock_project/a.py")
