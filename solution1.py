import argparse

from lxml import html

from utils import clean, create_url, get_response, write_data_to_csv


def parse(zipcode, filter=None):
    url = create_url(zipcode, filter)
    response = get_response(url)

    if not response:
        print(
            "Failed to fetch the page, please check `response.html` to see the response received from zillow.com."
        )
        return None

    parser = html.fromstring(response.text)
    search_results = parser.xpath("//div[@id='grid-search-results']//article")
    print(search_results)

    print("parsing from html page")
    properties_list = []
    for properties in search_results:
        raw_address = properties.xpath(".//address//text()")
        raw_price = properties.xpath(
            ".//span[@class='PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr']//text()"
        )
        raw_broker_name = properties.xpath(
            ".//div[@class='StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 jretvB']//text()"
        )
        url = properties.xpath(
            ".//a[@class='StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 jnnxAW property-card-link']/@href"
        )
        raw_title = properties.xpath(".//h4//text()")
        address = clean(raw_address)
        price = clean(raw_price)
        # info = clean(raw_info).replace(u"\xb7", ',')
        broker = clean(raw_broker_name)
        title = clean(raw_title)
        property_url = "https://www.zillow.com" + url[0] if url else None
        properties = {
            "address": address,
            "price": price,
            "real estate provider": broker,
            "url": property_url,
        }
        print(properties)
        properties_list.append(properties)
    return properties_list


if __name__ == "__main__":
    # Reading arguments

    argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument("zipcode", help="")
    sortorder_help = """
    available sort orders are :
    newest : Latest property details,
    cheapest : Properties with cheapest price
    """

    argparser.add_argument(
        "sort", nargs="?", help=sortorder_help, default="Homes For You"
    )
    args = argparser.parse_args()
    zipcode = args.zipcode
    sort = args.sort
    print("Fetching data for %s" % (zipcode))
    scraped_data = parse(zipcode, sort)
    if scraped_data:
        print("Writing data to output file")
        write_data_to_csv(scraped_data, zipcode)
