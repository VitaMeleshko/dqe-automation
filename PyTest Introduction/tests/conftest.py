import os

import pytest
import pandas as pd

# Fixture to read the CSV file
@pytest.fixture(scope="module")
def csv_data():
    """
    read csv file and return dataframe
    Scope: module
    Returns: pd.DataFrame
    """
    # path to csv file
    csv_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "src",
        "data",
        "data.csv"
    )
    # check that csv file exist
    if not os.path.exists(csv_path):
        pytest.fail(f"CSV file is not found: {csv_path}")
    # read csv file
    df = pd.read_csv(csv_path)

    return df
# Fixture to validate the schema of the file
@pytest.fixture
def expected_schema():
    """
    return expected file's schema
    Returns: list of columns
    """
    return ['id', 'name', 'age', 'email', 'is_active']

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