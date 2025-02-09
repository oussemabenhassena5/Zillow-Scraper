import csv
import requests
import time
import random


def clean(text):
    if text:
        return " ".join(" ".join(text).split())
    return None


def get_headers():
    return {
        "authority": "www.zillow.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": '"Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }


def create_url(zipcode, filter):
    # Creating Zillow URL based on the filter.

    if filter == "newest":
        url = (
            "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/days_sort".format(
                zipcode
            )
        )
    elif filter == "cheapest":
        url = "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/pricea_sort/".format(
            zipcode
        )
    else:
        url = "https://www.zillow.com/homes/for_sale/{0}_rb/?fromHomePage=true&amp;shouldFireSellPageImplicitClaimGA=false&amp;fromHomePageTab=buy".format(
            zipcode
        )
    print(url)
    return url


def save_to_file(response):
    with open("response.html", "w", encoding="utf-8") as fp:
        fp.write(response.text)


def write_data_to_csv(data, zipcode):
    with open("properties-%s.csv" % (zipcode), "wb") as csvfile:
        fieldnames = ["address", "price", "real estate provider", "url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def get_response(url):
    session = requests.Session()
    for i in range(3):  # Reduce retries
        try:
            response = session.get(url, headers=get_headers(), timeout=10)
            print("Status code:", response.status_code)
            if response.status_code == 200:
                save_to_file(response)
                return response
            # Add random delay
            time.sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"Request failed: {str(e)}")
            time.sleep(random.uniform(2, 5))
    return None
