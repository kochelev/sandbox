import pytest

@pytest.fixture()
def fixture_from_another_file() -> int:
    return 10
