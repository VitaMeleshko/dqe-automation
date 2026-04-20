import pytest
import pandas as pd

# Fixture to load csv file and returns DataFrame
@pytest.fixture(scope="session")
def read_csv_data(request):
    def _read_csv(path):

        return pd.read_csv(path)

    return _read_csv

# Fixture that compares two schemas (actual and expected)
@pytest.fixture
def validate_schema():
    def _compare_schemas(actual_schema, expected_schema):
        assert actual_schema == expected_schema, (
            f"Schema is incorrect\n"
            f"Expected: {expected_schema}\n"
            f"Actual: {actual_schema}"
        )
    return _compare_schemas

# Pytest hook to mark unmarked tests with a custom mark
def pytest_collection_modifyitems(items):
    """
    hook assign tests without marks to a custom mark:unmarked.
    """
    for item in items:
        # Check that test has mark
        if not list(item.iter_markers()):
            # If test does not have mark add "unmarked"
            item.add_marker(pytest.mark.unmarked)