"""
This file initializes the web browser and runs the web crawler.
"""

import web_crawler
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def setup_browser():
    """
    Configures and initializes a Firefox browser instance with appropriate settings.
    """
    binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("pdfjs.disabled", True)
    return webdriver.Firefox(firefox_profile=profile, firefox_binary=binary)


def run_crawler():
    """
    Initializes the browser and executes the crawling function.
    """
    browser = setup_browser()

    try:
        # Start crawling
        Crawler.crawling_in_my_skin(browser)
    except Exception as e:
        print(f"An error occurred during crawling: {e}")
    finally:
        # Ensure browser is closed after crawling
        browser.quit()
