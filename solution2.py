from selenium import webdriver
from selenium_stealth import stealth
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv
import json
import os


class ZillowScraper:
    def __init__(self):
        # Set up Chrome options
        options = uc.ChromeOptions()

        # Add required arguments
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--enable-javascript")

        # Initialize the driver and specify your Chrome version (major version 132)
        self.driver = uc.Chrome(options=options, version_main=132)

        # Apply stealth settings
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        # Set up wait
        self.wait = WebDriverWait(self.driver, 20)

    def _random_sleep(self, min_time=2, max_time=5):
        time.sleep(random.uniform(min_time, max_time))

    def _scroll_page(self):
        """Scroll the page slowly to simulate human behavior"""
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(1, total_height, random.randint(100, 200)):
            self.driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(random.uniform(0.1, 0.3))

    def create_url(self, zipcode, filter_type="newest"):
        """Create URL based on filter type"""
        base_url = f"https://www.zillow.com/homes/{zipcode}_rb/"
        if filter_type == "newest":
            return f"{base_url}?sortBy=days&direction=asc"
        elif filter_type == "cheapest":
            return f"{base_url}?sortBy=price&direction=asc"
        return base_url

    def extract_property_data(self):
        properties = []
        try:
            # Wait for property cards to load
            property_cards = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "article.list-card")
                )
            )

            for card in property_cards:
                try:
                    # Extract property details with explicit waits
                    price = self.wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, ".list-card-price")
                        )
                    ).text

                    address = self.wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, ".list-card-addr")
                        )
                    ).text

                    # Get additional details
                    details = card.find_element(
                        By.CSS_SELECTOR, ".list-card-details"
                    ).text

                    # Get link
                    link = card.find_element(
                        By.CSS_SELECTOR, "a.list-card-link"
                    ).get_attribute("href")

                    properties.append(
                        {
                            "price": price,
                            "address": address,
                            "details": details,
                            "url": link,
                        }
                    )

                except Exception as e:
                    print(f"Error extracting property data: {str(e)}")
                    continue

            return properties

        except Exception as e:
            print(f"Error in property extraction: {str(e)}")
            return []

    def scrape(self, zipcode, filter_type="newest", max_retries=3):
        url = self.create_url(zipcode, filter_type)

        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1} of {max_retries}")

                # Load the page
                self.driver.get(url)
                self._random_sleep(3, 6)

                # Handle initial page load
                self._scroll_page()
                self._random_sleep(2, 4)

                # Extract properties
                properties = self.extract_property_data()

                if properties:
                    print(f"Successfully scraped {len(properties)} properties")
                    return properties

            except Exception as e:
                print(f"Error during scraping: {str(e)}")
                self._random_sleep(5, 10)

        return []

    def save_to_csv(self, properties, filename=None):
        if not properties:
            print("No properties to save")
            return

        if not filename:
            filename = f"zillow_properties_{int(time.time())}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=properties[0].keys())
            writer.writeheader()
            writer.writerows(properties)

        print(f"Saved {len(properties)} properties to {filename}")

    def close(self):
        self.driver.quit()


def main():
    scraper = None  # Initialize scraper to ensure it's defined
    try:
        scraper = ZillowScraper()
        zipcode = input("Enter ZIP code to search: ")
        filter_type = input("Enter filter type (newest/cheapest/default): ") or "newest"

        properties = scraper.scrape(zipcode, filter_type)

        if properties:
            filename = f"zillow_{zipcode}_{filter_type}.csv"
            scraper.save_to_csv(properties, filename)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if scraper is not None:
            scraper.close()


if __name__ == "__main__":
    main()
