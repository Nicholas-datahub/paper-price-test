# Estrutura base do scraper para os indicadores Caixin Services Index, Bloomberg Commodity Index e USD/CNY
# Arquivo: scraper/main_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from google.cloud import storage

BUCKET_NAME = os.getenv("GCS_BUCKET", "investing-data-bucket")


def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)


def scrape_caixin_services_index():
    url = "https://br.investing.com/economic-calendar/chinese-caixin-services-pmi-596"
    driver = get_chrome_driver()
    driver.get(url)
    time.sleep(10)
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


def scrape_bloomberg_index():
    url = "https://br.investing.com/indices/bloomberg-commodity-historical-data"
    driver = get_chrome_driver()
    driver.get(url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    table = soup.find("table", {"id": "curr_table"})
    rows = table.find_all("tr")
    data = []
    for row in rows[1:]:
        cols = [td.text.strip().replace(",", "") for td in row.find_all("td")]
        if len(cols) == 6:
            date, close, open_, high, low, volume = cols
            data.append([date, close, open_, high, low, volume])
    df = pd.DataFrame(data, columns=["date", "close", "open", "high", "low", "volume"])
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    return df


def scrape_usd_cny():
    url = "https://br.investing.com/currencies/usd-cny-historical-data"
    driver = get_chrome_driver()
    driver.get(url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    table = soup.find("table", {"id": "curr_table"})
    rows = table.find_all("tr")
    data = []
    for row in rows[1:]:
        cols = [td.text.strip().replace(",", "") for td in row.find_all("td")]
        if len(cols) == 6:
            date, close, open_, high, low, volume = cols
            data.append([date, close, open_, high, low, volume])
    df = pd.DataFrame(data, columns=["date", "close", "open", "high", "low", "volume"])
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    return df


def save_to_gcs(df, filename):
    df.to_csv(filename, index=False)
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"raw/{filename}")
    blob.upload_from_filename(filename)


def main():
    df_caixin = scrape_caixin_services_index()
    save_to_gcs(df_caixin, filename="caixin_index.csv")

    df_bloomberg = scrape_bloomberg_index()
    save_to_gcs(df_bloomberg, filename="bloomberg_commodity_index.csv")

    df_usd_cny = scrape_usd_cny()
    save_to_gcs(df_usd_cny, filename="usd_cny.csv")


if __name__ == "__main__":
    main()
