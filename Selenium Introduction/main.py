import os
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException



class DriverManager:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        # Start Chrome
        self.driver = webdriver.Chrome()
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the browser
        if self.driver:
            self.driver.quit()
        return False

def save_table_to_csv(driver, filename="table.csv", take_first_columns=3, take_first_rows=10):
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "table"))
    )

    driver.find_element(By.CSS_SELECTOR, "g.table")

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

    # 10) Записуємо у CSV
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def save_doughnut_to_csv(driver, filename):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "pielayer"))
    )

    doughnut = driver.find_element(By.CLASS_NAME, "pielayer")

    labels = doughnut.find_elements(By.CSS_SELECTOR, "text.slicetext[data-notex='1']")

    rows = []
    for label in labels:
        # 4) every label - 2 rows (tspan):
        #    - Facility Type
        #    - Min Average Time Spent
        tspans = label.find_elements(By.TAG_NAME, "tspan")

        if len(tspans) >= 2:
            category = tspans[0].text.strip()
            value = tspans[1].text.strip()

            if category and value:
                rows.append([category, value])

    # 5) Write CSV
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Facility Type", "Min Average Time Spent"])
        writer.writerows(rows)

def screenshot_chart(driver, filename):
    # Find container of the chart
    chart_div = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'plotly-graph-div')]")
        )
    )
    # Screenshot
    chart_div.screenshot(filename)


if __name__ == "__main__":
     # Folder for results
    RESULT_DIR = "result"
    os.makedirs(RESULT_DIR, exist_ok=True)

    # Шлях до HTML репорту
    html_path = os.path.join("generated_report", "report.html")

    # Selenium відкриває локальні html через file:// + absolute path
    file_url = "file://" + os.path.abspath(html_path)

    with DriverManager() as driver:
        driver.get(file_url)

        try:
            save_table_to_csv(driver, "table.csv")
            print("OK: table.csv saved")
        except (TimeoutException, NoSuchElementException) as e:
            # TimeoutException: don't load elelemt
            # NoSuchElementException: Element is not found
            print("ERROR: cannot read table:", e)

         # DOUGHNUT -> screenshots + doughnut*.csv
        try:
            # First stage
            screenshot_chart(driver, os.path.join(RESULT_DIR, "screenshot0.png"))
            save_doughnut_to_csv(driver, os.path.join(RESULT_DIR, "doughnut0.csv"))
            print("OK: screenshot0.png, doughnut0.csv")

            # Wait legend
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "scrollbox")))
            legend_box = driver.find_element(By.CLASS_NAME, "scrollbox")

            # Lagend's items than can be clicked
            legend_items = legend_box.find_elements(By.CLASS_NAME, "traces")

            #- DOUBLE CLICK on legend -> one element is isolated
            # - DOUBLE CLICK -> came back
            actions = ActionChains(driver)

            for i, item in enumerate(legend_items, start=1):
                try:
                    # One sector is isolated
                    actions.double_click(item).perform()
                    time.sleep(1)

                    screenshot_chart(driver, os.path.join(RESULT_DIR,f"screenshot{i}.png"))
                    save_doughnut_to_csv(driver, os.path.join(RESULT_DIR,f"doughnut{i}.csv"))
                    print(f"OK: screenshot{i}.png, doughnut{i}.csv")

                    # came back "ALL"
                    actions.double_click(item).perform()
                    time.sleep(1)

                except Exception as e:
                    print(f"WARNING: filter #{i} failed:", e)

        except (TimeoutException, NoSuchElementException) as e:
            print("ERROR: cannot work with doughnut chart/legend:", e)