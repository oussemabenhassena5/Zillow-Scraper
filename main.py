# scraper.py
import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def get_properties(zip_code, max_pages=3):
    properties = []

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}")
        url = f"https://www.zillow.com/homes/{zip_code}_rb/?page={page}"

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        listings = soup.find_all(
            "li",
            class_="ListItem-c11n-8-109-1__sc-13rwu5a-0 StyledListCardWrapper-srp-8-109-1__sc-wtsrtn-0 bvHMyj khcxqR",
        )

        for listing in listings:
            try:
                price = listing.find(
                    "span",
                    class_="PropertyCardWrapper__StyledPriceLine-srp-8-109-1__sc-16e8gqd-1 btjnz",
                ).text.strip()
                address = listing.find("address", class_="list-card-addr").text.strip()
                details = listing.find(
                    "div",
                    class_="StyledPropertyCardDataArea-c11n-8-109-1__sc-10i1r6-0 kcntXk",
                ).text.strip()
                link = listing.find(
                    "a",
                    class_="StyledPropertyCardDataArea-c11n-8-109-1__sc-10i1r6-0 cypVEL property-card-link",
                )["href"]

                if not link.startswith("http"):
                    link = f"https://www.zillow.com{link}"

                properties.append(
                    {
                        "price": price,
                        "address": address,
                        "details": details,
                        "link": link,
                    }
                )
            except AttributeError as e:
                print(f"Error parsing listing: {e}")
                continue

        # Random delay to be polite
        sleep(random.uniform(1, 3))

    return properties


def save_to_csv(data, filename="properties.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["price", "address", "details", "link"])
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    zip_code = input("Enter ZIP code to search: ")
    properties = get_properties(zip_code)
    save_to_csv(properties)
    print(f"Saved {len(properties)} properties to properties.csv")
