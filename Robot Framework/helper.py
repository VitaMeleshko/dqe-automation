# helper.py
import json
from pathlib import Path
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from robot.libraries.BuiltIn import BuiltIn


# Get WebDriver

def get_webdriver_instance():
    se_lib = BuiltIn().get_library_instance('SeleniumLibrary')
    return se_lib.driver


# ========== HTML -> DataFrame (Selenium) ==========

def read_html_table_to_df(driver) -> pd.DataFrame:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "table"))
    )

    driver.find_element(By.CSS_SELECTOR, "g.table")

    table = driver.find_element(By.CLASS_NAME, "table")

    columns = table.find_elements(By.CLASS_NAME, "y-column")[:3]

    headers = []
    all_values = []

    for col in columns:
        header_text = col.find_element(By.ID, "header").text.strip()
        headers.append(header_text)

        cells = col.find_elements(By.CLASS_NAME, "cell-text")

        values = []
        for c in cells:
            text = c.text.strip()
            if text and text != header_text:
                values.append(text)

        all_values.append(values[:20])

    rows = list(zip(*all_values))

    df = pd.DataFrame(rows, columns=headers)

    # Convert to same format as Parquet
    df["Average Time Spent"] = pd.to_numeric(df["Average Time Spent"])

    return df


# ========== Parquet -> DataFrame ==========

COLUMN_MAP = {
    "facility_type": "Facility Type",
    "visit_date": "Visit Date",
    "avg_time_spent": "Average Time Spent",
}


def read_parquet_to_df(parquet_root: str, filter_date: str = "") -> pd.DataFrame:
    root = Path(parquet_root)

    files = list(root.rglob("*.parquet"))

    df = pd.concat([pd.read_parquet(f, engine="pyarrow") for f in files], ignore_index=True)

    df = df.rename(columns=COLUMN_MAP)

    if filter_date:
        df["Visit Date"] = pd.to_datetime(df["Visit Date"])
        df = df[df["Visit Date"] >= pd.to_datetime(filter_date)]
        df["Visit Date"] = df["Visit Date"].dt.strftime("%Y-%m-%d")

    df = df[["Facility Type", "Visit Date", "Average Time Spent"]]

    return df


# ========== Compare ==========

def compare_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> tuple:
    df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
    df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)

    # Check if DataFrames are exactly equal
    if df1_sorted.equals(df2_sorted):
        return True, ""

    # Show data differences
    comparison = df1_sorted.compare(df2_sorted, keep_equal=False)
    diff_report = f"Data differences (first 30 rows):\n{comparison.head(30).to_string()}"

    return False, diff_report