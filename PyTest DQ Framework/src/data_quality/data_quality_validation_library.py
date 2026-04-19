
class DataQualityLibrary:
    """
    A library of static methods for performing data quality checks on pandas DataFrames.

    This class is intended to be used in a PyTest-based testing framework to validate
    the quality of data in DataFrames. Each method performs a specific data quality
    check and uses assertions to ensure that the data meets the expected conditions.
    """

    @staticmethod
    def check_duplicates(df, column_names=None):
        if column_names:
            duplicates = df.duplicated(subset=column_names, keep=False)
        else:
            duplicates = df.duplicated(keep=False)

        duplicate_count = duplicates.sum()
        assert duplicate_count == 0, f"Found {duplicate_count} duplicate rows"


    @staticmethod
    def check_count(df1, df2):

        count1 = len(df1)
        count2 = len(df2)

        assert count1 == count2, f"Row count mismatch: df1={count1}, df2={count2}"


    @staticmethod
    def check_data_full_data_set(df1, df2):

        # Comparing
        assert df1.equals(df2), "Data are not equal"

    @staticmethod
    def check_dataset_is_not_empty(df):

        row_count = len(df)

        assert row_count > 0, f"DataFrame is empty (row count: {row_count})"

    @staticmethod
    def check_not_null_values(df, column_names=None):
        if column_names is None:
            column_names = df.columns.tolist()

        for col in column_names:
            null_count = df[col].isnull().sum()
            assert null_count == 0, f"Column '{col}' contains {null_count} NULL values"