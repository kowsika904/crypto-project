from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def setup_driver():
    print("Opening Chrome Browser...")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # Optional headless mode
    # chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver


def scrape_crypto_data(driver):
    print("Opening CoinMarketCap Website...")

    driver.get("https://coinmarketcap.com/")

    print("Loading page...")
    time.sleep(5)

    crypto_data = []

    try:
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")[:10]

        print("\nCollecting Top 10 Cryptocurrency Data...\n")

        for row in rows:
            try:
                name = row.find_element(By.XPATH, ".//td[3]//p").text
                price = row.find_element(By.XPATH, ".//td[4]").text
                change_24h = row.find_element(By.XPATH, ".//td[5]").text
                market_cap = row.find_element(By.XPATH, ".//td[8]").text

                crypto_data.append({
                    "Coin Name": name,
                    "Current Price": price,
                    "24h Change": change_24h,
                    "Market Cap": market_cap
                })

                print(f"Collected: {name}")

            except Exception as row_error:
                print("Row Error:", row_error)

    except Exception as main_error:
        print("Scraping Error:", main_error)

    return crypto_data


def save_to_csv(data):
    print("\nSaving data to CSV...")

    df = pd.DataFrame(data)
    file_name = "crypto_prices.csv"
    df.to_csv(file_name, index=False)

    print(f"Data saved successfully in {file_name}")


def main():
    print("🚀 Cryptocurrency Price Tracker Started...\n")

    driver = setup_driver()

    try:
        data = scrape_crypto_data(driver)

        if data:
            save_to_csv(data)
        else:
            print("No data found.")

    finally:
        driver.quit()
        print("\nBrowser closed successfully.")


if __name__ == "__main__":
    main()