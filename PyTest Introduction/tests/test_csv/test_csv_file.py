import pytest

# Validate that file is not empty.
def test_file_not_empty(csv_data):
    assert len(csv_data) > 0, "csv file is epty"

# Validate there are no duplicate rows.
@pytest.mark.validate_csv
@pytest.mark.xfail
def test_duplicates(csv_data):
    duplicates = csv_data[csv_data.duplicated()]
    assert duplicates.empty, \
        f"Found {len(duplicates)} dublicates:\n{duplicates}"

# Validate the schema of the file (id, name, age, email, is_active).
@pytest.mark.validate_csv
def test_validate_schema(csv_data, expected_schema):
    actual_columns = list(csv_data.columns)
    assert actual_columns == expected_schema, (
        f"Schema is incorrect\n"
        f"Expected: {expected_schema}\n"
        f"Actual: {actual_columns}"
    )

# Validate that the age column contains valid values (0-100).
@pytest.mark.validate_csv
@pytest.mark.skip
def test_age_column_valid(csv_data):

    assert csv_data['age'].between(0,100).all(), "Column age contains invalid values "

# Validate that the email column contains valid email addresses (format).
@pytest.mark.validate_csv
def test_email_column_valid(csv_data):
    # regexp for validating of emails format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # match emails with email's format
    invalid_emails = csv_data[~csv_data['email'].str.match(email_pattern, na=False)]

    assert invalid_emails.empty, f"Invalid emails {invalid_emails['email']}"

# Test with paramatrization. Validate: is_active = False for id = 1; is_active = True for id = 2
@pytest.mark.parametrize("user_id, expected_is_active", [
    (1, False),  # Check for id=1 is is_active=False
    (2, True),   # Check for id=2 is is_active=True
])
def test_active_players(csv_data, user_id, expected_is_active):
    # Find row with user_id
    user_row = csv_data[csv_data['id'] == user_id]

    # Value is_active for user_id
    actual_is_active = user_row.iloc[0]['is_active']

    assert actual_is_active == expected_is_active, (
        f"For id={user_id} expected result: is_active={expected_is_active},\
        actual result: is_active={actual_is_active}"
    )

# Same as previous one for id = 2, but without parametrized mark.
def test_active_player(csv_data):
    # Find row with id = 2
    user_row = csv_data[csv_data['id'] == 2]

    # Value is_active for id = 2
    actual_is_active = user_row.iloc[0]['is_active']

    assert actual_is_active == True, (
            f"For id=2 is_active={actual_is_active} "
    )
