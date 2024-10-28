"""
This file serves as the main entry point for the program.
"""

import os
import form_filler
from run_crawler import run_crawler, setup_browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Directory and file paths
URLS_DIR = r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs"
URLS_FILE = os.path.join(URLS_DIR, "urls_disposiciones.txt")


def format_direcciones(file_path):
    """
    Reads URLs from the specified file and strips whitespace.
    """
    with open(file_path) as file:
        return [line.strip() for line in file]


def main():
    # Check if URL file exists and has content; if not, run the crawler
    if not os.path.exists(URLS_FILE) or os.stat(URLS_FILE).st_size == 0:
        print("No URLs found. Running crawler to populate URLs...")
        run_crawler()

    # Load URLs from file
    processed_urls = format_direcciones(URLS_FILE)

    # Start browser and log in
    browser = setup_browser()
    browser.get("http://magislex.com/")
    FormFiller.log_in(browser)
    FormFiller.in_disposiciones(browser)

    # Focus on main frame content
    browser.switch_to.default_content()
    browser.switch_to.frame("mainFrame")
    browser.switch_to.frame("contenidoFrame")
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                 "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)")))

    # Iterate through URLs to process each
    for url in processed_urls[:]:  # Copy list to allow modification during iteration
        try:
            # Reset previous disposition data and open URL in new tab
            FormFiller.reset_datos_disposicion()
            browser.execute_script(f"window.open('{url}');")
            browser.switch_to.window(browser.window_handles[1])

            # Read and process the disposition
            FormFiller.read_disposicion_html(url, browser)
            browser.close()  # Close current tab after processing
            browser.switch_to.window(browser.window_handles[0])  # Return to main tab

            # Fill and submit the form
            FormFiller.fill_form(FormFiller.datos_disposicion, browser)
            FormFiller.back_to_disposiciones(browser)

            # Mark URL as processed
            processed_urls.remove(url)

        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            continue  # Skip to next URL if an error occurs

    # Optionally save remaining URLs for retry in case of errors
    with open(URLS_FILE, "w") as file:
        file.writelines([url + "\n" for url in processed_urls])

    browser.quit()


if __name__ == "__main__":
    main()
