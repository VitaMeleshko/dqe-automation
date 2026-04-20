"""
Description: Data Quality checks for facility_type_avg_time_spent_per_visit_date dataset
Requirement(s): TICKET-1235
Author(s): Vita Meleshko
"""
import pytest

@pytest.fixture(scope='module')
def source_data(db_connection):
    """
    Get data from  PostgreSQL (source).
    """
    source_query = """
    SELECT 
        f.facility_name,
        DATE(v.visit_timestamp) as visit_date,
        MIN(v.duration_minutes) as min_time_spent
    FROM visits v
    JOIN facilities f ON v.facility_id = f.id
    GROUP BY f.facility_name, DATE(v.visit_timestamp)
    ORDER BY f.facility_name, DATE(v.visit_timestamp)
    """
    source_data = db_connection.get_data_sql(source_query)
    return source_data

@pytest.fixture(scope='module')
def target_data(parquet_reader):
    """
    read data from  Parquet files (target).
    """
    target_path = '/parquet_data/facility_name_min_time_spent_per_visit_date'
    target_data = parquet_reader.process(target_path, include_subfolders=True)

    # Remove partition_date (created for partitioning)
    if 'partition_date' in target_data.columns:
        target_data = target_data.drop(columns=['partition_date'])

    return target_data


@pytest.mark.parquet_data
@pytest.mark.smoke
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_dataset_is_not_empty(target_data, data_quality_library):
    """Validate that data set is not empty"""
    data_quality_library.check_dataset_is_not_empty(target_data)


@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_count(source_data, target_data, data_quality_library):
    """Validate that source and target have the same row count"""
    data_quality_library.check_count(source_data, target_data)


@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_data_full_data_set(source_data, target_data, data_quality_library):
    """Validate that all data from source is present in target"""
    data_quality_library.check_data_full_data_set(source_data, target_data)


@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_duplicates(target_data, data_quality_library):
    """Validate that there are no duplicate rows in target dataset"""
    data_quality_library.check_duplicates(target_data)


@pytest.mark.parquet_data
@pytest.mark.facility_type_avg_time_spent_per_visit_date
def test_check_not_null_values(target_data, data_quality_library):
    """Validate that critical columns do not contain NULL values"""
    data_quality_library.check_not_null_values(
        target_data,
        ['facility_type', 'visit_date', 'avg_time_spent']
    )