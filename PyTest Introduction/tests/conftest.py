import os
from pathlib import Path

import pytest
import pandas as pd
# Fixture to  provide path to CSV file.
@pytest.fixture(scope="session")
def path_to_file():

    return Path(__file__).parent.parent / "src" / "data" / "data.csv"

# Fixture to load csv file and returns DataFrame
@pytest.fixture(scope="session")
def read_csv_data(path_to_file):

    df = pd.read_csv(path_to_file)

    return df
# Fixture to get the expected schema of the file
@pytest.fixture(scope="session")
def expected_schema():
    """
    return expected file's schema
    Returns: list of columns
    """
    return ['id', 'name', 'age', 'email', 'is_active']

# Fixture to get the actual schema of the file
@pytest.fixture(scope="session")
def actual_schema(read_csv_data):

    return list(read_csv_data.columns)

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