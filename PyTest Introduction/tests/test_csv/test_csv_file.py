import pytest
from pathlib import Path

# Path to file
path_to_file = Path(__file__).parent.parent.parent / "src" / "data" / "data.csv"

# expected schema
expected_schema = ['id', 'name', 'age', 'email', 'is_active']

# Validate that file is not empty.
def test_file_not_empty(read_csv_data):
    df = read_csv_data(path_to_file)
    assert len(df) > 0, "csv file is empty"

# Validate there are no duplicate rows.
@pytest.mark.validate_csv
@pytest.mark.xfail
def test_duplicates(read_csv_data):
    df = read_csv_data(path_to_file)
    duplicates = df[df.duplicated()]
    assert duplicates.empty, \
        f"Found {len(duplicates)} dublicates:\n{duplicates}"

# Validate the schema of the file (id, name, age, email, is_active).
@pytest.mark.validate_csv
def test_validate_schema(read_csv_data, validate_schema):
    df = read_csv_data(path_to_file)
    actual_schema = list(df.columns)
    # Use fixture to compare actual and expected schema
    validate_schema(actual_schema, expected_schema)


# Validate that the age column contains valid values (0-100).
@pytest.mark.validate_csv
@pytest.mark.skip
def test_age_column_valid(read_csv_data):
    df = read_csv_data(path_to_file)
    assert df['age'].between(0,100).all(), "Column age contains invalid values "

# Validate that the email column contains valid email addresses (format).
@pytest.mark.validate_csv
def test_email_column_valid(read_csv_data):
    df = read_csv_data(path_to_file)
    # regexp for validating of emails format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # match emails with email's format
    invalid_emails = df[~df['email'].str.match(email_pattern, na=False)]
    assert invalid_emails.empty, f"Invalid emails {invalid_emails['email']}"

# Test with paramatrization. Validate: is_active = False for id = 1; is_active = True for id = 2
@pytest.mark.parametrize("user_id, expected_is_active", [
    (1, False),  # Check for id=1 is is_active=False
    (2, True),   # Check for id=2 is is_active=True
])
def test_active_players(read_csv_data, user_id, expected_is_active):
    df = read_csv_data(path_to_file)
    # Find row with user_id
    user_row = df[df['id'] == user_id]
    # Value is_active for user_id
    actual_is_active = user_row.iloc[0]['is_active']
    assert actual_is_active == expected_is_active, (
        f"For id={user_id} expected result: is_active={expected_is_active},\
        actual result: is_active={actual_is_active}"
    )

# Same as previous one for id = 2, but without parametrized mark.
def test_active_player(read_csv_data):
    df = read_csv_data(path_to_file)
    # Find row with id = 2
    user_row = df[df['id'] == 2]
    # Value is_active for id = 2
    actual_is_active = user_row.iloc[0]['is_active']
    assert actual_is_active == True, (
            f"For id=2 expected result: is_active = True,\
            actual result: is_active={actual_is_active} "
    )
