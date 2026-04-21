"""
Description: Data Quality checks for patient_sum_treatment_cost_per_facility_type dataset
Requirement(s): TICKET-1236
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
        f.facility_type,
        CONCAT(p.first_name, ' ', p.last_name) AS full_name,
        SUM(v.treatment_cost) as sum_treatment_cost
    FROM visits v
    JOIN facilities f ON v.facility_id = f.id
    JOIN patients p  ON p.id = v.patient_id
    GROUP BY  f.facility_type, full_name
    """
    source_data = db_connection.get_data_sql(source_query)
    return source_data


@pytest.fixture(scope='module')
def target_data(parquet_reader):
    """
    read data from  Parquet files (target).
    """
    target_path = '/parquet_data/patient_sum_treatment_cost_per_facility_type'
    target_data = parquet_reader.process(target_path, include_subfolders=True)

    # Remove partition_date (created for partitioning)
    if 'facility_type_partition' in target_data.columns:
        target_data = target_data.drop(columns=['facility_type_partition'])

    return target_data


@pytest.mark.parquet_data
@pytest.mark.smoke
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_check_dataset_is_not_empty(target_data, data_quality_library):
    """Validate that target dataset is not empty"""
    data_quality_library.check_dataset_is_not_empty(target_data)


@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_check_count(source_data, target_data, data_quality_library):
    """Validate that source and target have the same row count"""
    data_quality_library.check_count(source_data, target_data)


@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_check_data_full_data_set(source_data, target_data, data_quality_library):
    """Validate that source and target datasets are identical"""
    data_quality_library.check_data_full_data_set(source_data, target_data)


@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_check_duplicates(target_data, data_quality_library):
    """Validate that there are no duplicate rows in target dataset"""
    data_quality_library.check_duplicates(target_data)


@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_check_not_null_values(target_data, data_quality_library):
    """Validate that critical columns do not contain NULL values"""
    data_quality_library.check_not_null_values(
        target_data,
        [ 'facility_type', 'full_name', 'sum_treatment_cost']
    )