import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class SeleniumWebDriverContextManager:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        self.driver = webdriver.Chrome()
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
        return False


def extract_table(driver, filename="table.csv", take_first_columns=3, take_first_rows=10):
    """Extract table data and save to CSV"""
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "table"))
        )

        table = driver.find_element(By.CLASS_NAME, "table")
        columns = table.find_elements(By.CLASS_NAME, "y-column")[:take_first_columns]

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

            all_values.append(values[:take_first_rows])

        rows = list(zip(*all_values))

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"OK: {filename} saved")
    except (TimeoutException, NoSuchElementException) as e:
        print(f"ERROR: cannot read table: {e}")


def extract_doughnut_chart(driver, result_dir="results"):
    """Extract doughnut chart data with screenshots"""
    try:
        # Initial screenshot and CSV
        screenshot_chart(driver, os.path.join(result_dir, "screenshot0.png"))
        save_doughnut_to_csv(driver, os.path.join(result_dir, "doughnut0.csv"))
        print("OK: screenshot0.png, doughnut0.csv")

        # Wait for legend
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scrollbox"))
        )
        legend_box = driver.find_element(By.CLASS_NAME, "scrollbox")
        legend_items = legend_box.find_elements(By.CLASS_NAME, "traces")

        # Click each legend item
        for i, item in enumerate(legend_items, start=1):
            item.click()
            time.sleep(1)

            screenshot_chart(driver, os.path.join(result_dir, f"screenshot{i}.png"))
            save_doughnut_to_csv(driver, os.path.join(result_dir, f"doughnut{i}.csv"))
            print(f"OK: screenshot{i}.png, doughnut{i}.csv")

    except (TimeoutException, NoSuchElementException) as e:
        print(f"ERROR: cannot work with doughnut chart/legend: {e}")


def save_doughnut_to_csv(driver, filename):
    """Save doughnut chart data to CSV"""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "pielayer"))
    )

    doughnut = driver.find_element(By.CLASS_NAME, "pielayer")
    labels = doughnut.find_elements(By.CSS_SELECTOR, "text.slicetext[data-notex='1']")

    rows = []
    for label in labels:
        tspans = label.find_elements(By.TAG_NAME, "tspan")

        if len(tspans) >= 2:
            category = tspans[0].text.strip()
            value = tspans[1].text.strip()

            if category and value:
                rows.append([category, value])

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Facility Type", "Min Average Time Spent"])
        writer.writerows(rows)


def screenshot_chart(driver, filename):
    """Take screenshot of the chart"""
    chart_div = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'plotly-graph-div')]")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", chart_div)
    time.sleep(1.5)

    chart_div.screenshot(filename)


if __name__ == "__main__":
    RESULT_DIR = "results"
    os.makedirs(RESULT_DIR, exist_ok=True)

    with SeleniumWebDriverContextManager() as driver:
        # Open the HTML report file
        html_file_path = os.path.abspath("report.html")
        driver.get(f"file://{html_file_path}")

        # Zoom for screenshots
        driver.execute_script("document.body.style.zoom='100%'")
        time.sleep(0.5)

        # Extract table content
        extract_table(driver, "table.csv")

        # Extract doughnut chart data
        extract_doughnut_chart(driver, RESULT_DIR)