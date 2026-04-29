import json
from pathlib import Path

import pandas as pd


# ========== HTML -> DataFrame (Plotly table) ==========

def read_html_table_to_df(html: str) -> pd.DataFrame:
    # find place with plotly table
    pos = html.find('"type":"table"')
    if pos == -1:
        raise AssertionError('Plotly table not found')

    # extract section of HTML around table
    chunk = html[max(0, pos - 3000): pos + 3000]

    # extract column headers
    headers = json.loads(_extract_json_array_after(chunk, '"header"', '"values"'))
    # extract sell data
    cols    = json.loads(_extract_json_array_after(chunk, '"cells"',  '"values"'))

    # create dataframe: headers with column data
    df = pd.DataFrame({headers[i]: cols[i] for i in range(len(headers))})

    # Clean and standardize dataframe
    return _normalize_df(df)

# ========== Parquet -> DataFrame ==========

COLUMN_MAP = {
    "facility_type": "Facility Type",
    "visit_date": "Visit Date",
    "avg_time_spent": "Average Time Spent",
}

def read_parquet_to_df(parquet_root: str, filter_date: str = "") -> pd.DataFrame:
    root = Path(parquet_root)

    # Find all .parquet files in folder (including subfolders)
    files = list(root.rglob("*.parquet"))

    # Read all Parquet files and combine into one dataframe
    df = pd.concat([pd.read_parquet(f, engine="pyarrow") for f in files], ignore_index=True)

    # Rename columns to match HTML table
    df = df.rename(columns=COLUMN_MAP)

    # Filter by date
    if filter_date:
        df["Visit Date"] = pd.to_datetime(df["Visit Date"])
        df = df[df["Visit Date"] >= pd.to_datetime(filter_date)]
        df["Visit Date"] = df["Visit Date"].dt.strftime("%Y-%m-%d")

    # Ensure columns are in correct order
    df = df[["Facility Type", "Visit Date", "Average Time Spent"]]
    return _normalize_df(df)


# ========== Compare ==========

def dataframes_should_match_exactly(df_html: pd.DataFrame, df_parquet: pd.DataFrame):
    html_sorted = _sort_by_date_and_facility(_normalize_df(df_html))
    parquet_sorte = _sort_by_date_and_facility(_normalize_df(df_parquet))

    if list(html_sorted.columns) != list(parquet_sorte.columns):
        raise AssertionError(f"Columns differ:\nHTML: {list(html_sorted.columns)}\nParquet: {list(parquet_sorte.columns)}")

    if len(html_sorted) != len(parquet_sorte):
        raise AssertionError(f"Row count differs: HTML={len(html_sorted)} Parquet={len(parquet_sorte)}")

    if html_sorted.equals(parquet_sorte):
        return

    diff = html_sorted.compare(parquet_sorte, keep_equal=False)
    raise AssertionError("Data differs.\n" + diff.head(30).to_string())


# ========== Helper functions ==========

def _sort_by_date_and_facility(df: pd.DataFrame) -> pd.DataFrame:
    """Sort DataFrame by date and facility type for consistent comparison."""
    result = df.copy()

    # Convert "Visit Date" to datetime
    result["__temp_date"] = pd.to_datetime(result["Visit Date"], errors="raise")

    # Create numeric order for facility types
    facility_order = {"Clinic": 0, "Hospital": 1, "Specialty Center": 2}
    result["__temp_facility"] = result["Facility Type"].map(facility_order).fillna(999)

    # Sort by date first, then by facility type
    result = result.sort_values(
        by=["__temp_date", "__temp_facility"],
        ascending=[True, True]
    )

    # Remove temporary columns and reset index
    result = result.drop(columns=["__temp_date", "__temp_facility"])
    result = result.reset_index(drop=True)

    return result


def _extract_json_array_after(text: str, section_marker: str, key_marker: str) -> str:
    """
    Finds and extracts JSON array from text.

    Example: finds [...] after "header" and "values"
    """
    # Find section (e.g., "header")
    section_pos = text.find(section_marker)

    # Find key after section (e.g., "values")
    key_pos = text.find(key_marker, section_pos)

    # Find start of JSON array '['
    array_start = text.find('[', key_pos)

    # Find matching closing bracket ']'
    bracket_level = 0
    for i in range(array_start, len(text)):
        if text[i] == '[':
            bracket_level += 1
        elif text[i] == ']':
            bracket_level -= 1
            if bracket_level == 0:
                # Found matching closing bracket
                return text[array_start: i + 1]

    raise AssertionError("ERROR: Cannot find JSON array end ']' (unbalanced brackets)")


def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans and standardizes DataFrame for comparison."""
    result = df.copy()
    result = result.reset_index(drop=True)

    # Clean column names
    result.columns = [str(col).strip() for col in result.columns]

    # Convert all data to strings and trim whitespace
    result = result.astype("string")
    result = result.apply(lambda column: column.str.strip())

    return result