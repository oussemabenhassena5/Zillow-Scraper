# Zillow Scraper

**Status:** Work in Progress

## Overview
This project attempts to scrape property data from [Zillow](https://www.zillow.com/), including details such as price, address, and property specifics. The script uses Selenium with [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) and [selenium-stealth](https://github.com/diprajpatra/selenium-stealth) to bypass basic bot detection measures. However, Zillow employs advanced security techniques (e.g., CAPTCHAs, dynamic content loading, session validation) which can cause scraping attempts to fail or produce incomplete data.

> **Important:** This project is for educational and research purposes only. Scraping Zillow may violate their terms of service. Use this code responsibly and ensure that your activities comply with all applicable legal requirements.

## Features
- **Property Data Extraction:** Retrieves details such as price, address, property description, and URL.
- **Flexible Filtering:** Accepts a ZIP code as input and allows filtering by "newest" or "cheapest" listings.
- **CSV Output:** Saves the scraped data into a CSV file for further analysis.
- **Stealth Techniques:** Implements methods to mimic human browsing behavior (random sleep, scrolling) and utilizes stealth settings to bypass basic detection.

## Requirements
- **Python Version:** Python 3.8 or higher
- **Google Chrome:** A compatible version of Google Chrome must be installed.
  - **Note:** A version mismatch between Chrome and the ChromeDriver (managed by undetected-chromedriver) can lead to errors. For example, if your Chrome is version 132 while the driver supports version 133, you might encounter session creation errors.
- **Python Packages:**
  - `selenium`
  - `undetected-chromedriver`
  - `selenium-stealth`
  - Other dependencies as listed in `requirements.txt`

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/Zillow-Scraper.git
    cd Zillow-Scraper
    ```

2. **Set Up a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Scraper:**

    ```bash
    python3 main1.py
    ```

2. **Provide Input When Prompted:**
   - Enter the ZIP code you wish to search.
   - Choose the filter type by typing `newest`, `cheapest`, or press Enter for the default setting.

3. **Output:**
   - The scraper will process the Zillow page and attempt to extract property data.
   - If successful, the data will be saved in a CSV file named in the format: `zillow_<zipcode>_<filter_type>.csv`.

## Known Issues

- **Advanced Security Measures:** Zillow implements sophisticated anti-scraping mechanisms, such as CAPTCHAs and dynamic content changes. This means that scraping attempts might fail or require additional handling.
- **ChromeDriver Compatibility:** If you see errors like `session not created: This version of ChromeDriver only supports Chrome version X`, check that your installed Chrome version matches what `undetected-chromedriver` expects. You may need to either update Chrome or adjust the driver version by using the `version_main` parameter in your code.
- **Session Errors:** Issues such as "cannot connect to chrome" indicate problems with session creation, which might be related to the site's security measures or version mismatches.

## Future Work

- **Enhanced Evasion Techniques:** Investigate advanced methods such as rotating proxies, user-agent rotation, and CAPTCHA-solving services to better handle Zillow’s defenses.
- **Improved Error Handling:** Add more robust error and exception handling to better manage session errors and dynamic content issues.
- **Feature Expansion:** Include additional filters, more detailed data extraction, and support for other output formats.

## Contributing
Contributions to help improve this project are very welcome! If you have ideas or solutions to handle Zillow’s security measures more effectively, please open an issue or submit a pull request. When contributing, please ensure that your changes align with the educational and research-oriented nature of this project.

## Disclaimer
This project is provided **"as is"** without any warranties, express or implied. The authors are not liable for any misuse or damages arising from the use of this code. Ensure that you are aware of and comply with any legal obligations when using web scraping techniques.

## Contact
For any questions, suggestions, or contributions, please open an issue on GitHub or contact the repository maintainer.

---

*Use this project responsibly and at your own risk.*
