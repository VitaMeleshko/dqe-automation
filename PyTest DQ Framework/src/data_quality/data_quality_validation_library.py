
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
    def check_dataset_is_not_empty(df):

        row_count = len(df)

        assert row_count > 0, f"DataFrame is empty (row count: {row_count})"

    @staticmethod
    def check_data_full_data_set(df1, df2):
        df1_sorted = df1.sort_values(by=df1.columns.tolist()).reset_index(drop=True)
        df2_sorted = df2.sort_values(by=df2.columns.tolist()).reset_index(drop=True)

        if not df1_sorted.equals(df2_sorted):
            if len(df1_sorted) != len(df2_sorted):
                assert False, (
                    f"Row count mismatch:\n"
                    f"  df1: {len(df1)} rows, columns: {list(df1.columns)}\n"
                    f"  df2: {len(df2)} rows, columns: {list(df2.columns)}"
                )
            else:
                diff = df1_sorted.compare(df2_sorted)
                assert False, f"Data differences:\n{diff.head(10)}"


    @staticmethod
    def check_not_null_values(df, column_names=None):
        if column_names is None:
            column_names = df.columns.tolist()

        for col in column_names:
            try:
                null_count = df[col].isnull().sum()
                assert null_count == 0, f"Column '{col}' contains {null_count} NULL values"
            except KeyError:
                assert False, f"Column '{col}' does not exist in DataFrame. Available columns: {list(df.columns)}"