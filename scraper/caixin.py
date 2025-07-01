# Estrutura base do scraper para o indicador Caixin Services Index
# Arquivo: scraper/caixin.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from google.cloud import storage

BUCKET_NAME = os.getenv("GCS_BUCKET", "investing-data-bucket")


def scrape_caixin_services_index():
    url = "https://br.investing.com/economic-calendar/chinese-caixin-services-pmi-596"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(10)  # Aguarda o carregamento da tabela

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    table = soup.find("table", {"id": "economicCalendarData"})
    rows = table.find_all("tr", recursive=False)

    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 5:
            date = cols[0].text.strip()
            actual = cols[1].text.strip()
            forecast = cols[2].text.strip()
            previous = cols[3].text.strip()
            data.append([date, actual, previous, forecast])

    df = pd.DataFrame(data, columns=["date", "actual_state", "close", "forecast"])
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    return df


def save_to_gcs(df, filename="caixin_index.csv"):
    df.to_csv(filename, index=False)
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"raw/caixin/{filename}")
    blob.upload_from_filename(filename)


def main():
    df = scrape_caixin_services_index()
    save_to_gcs(df)


if __name__ == "__main__":
    main()
