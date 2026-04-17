import pandas as pd
from pathlib import Path

from pandas import DataFrame


class ParquetReader:
    """
    Class to read Parquet files.
    """

    def __init__(self):
        """Initialization"""
        pass

    def process(self, target_path: str, include_subfolders: bool = False) -> DataFrame | None:

        path = Path(target_path)

        # For file
        if path.is_file() and path.suffix == '.parquet':
            return pd.read_parquet(target_path)

        # For folder
        if path.is_dir():
            parquet_files = []

            if include_subfolders:
                # Recursive
                parquet_files = list(path.rglob('*.parquet'))
            else:
                # Only current folder
                parquet_files = list(path.glob('*.parquet'))

            if not parquet_files:
                raise FileNotFoundError(f"No Parquet files found in {target_path}")

            # Read files and concat
            dataframes = [pd.read_parquet(file) for file in parquet_files]
            return pd.concat(dataframes, ignore_index=True)

        raise FileNotFoundError(f"Path not found: {target_path}")