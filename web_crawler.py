"""
This file contains the logic for web crawling operations.
"""

import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time
import re
from datetime import date

# Define keywords to find relevant documents
KEYWORDS_TO_FIND = ["universid", "formación profesional", "educación", "educativo", "docente", "idiomas",
                    "enseñanza", "concierto educativo", "educación infantil", "educación secundaria",
                    "bachillerato", "erasmus", "profesor", "catedrático", "alumn"]

EXCLUDE_KEYWORDS = ["extravío", "anuncio de formalización", "personal de administración y servicios",
                    "libre designación", "asesor", "técnic", "contencioso-administrativo"]

# Main file path for saving URLs
SAVE_PATH = r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt"


def write_url(url):
    with open(SAVE_PATH, "a") as file:
        file.write(url + "\n")


def check_disposicion(text):
    text = text.lower()
    return any(keyword in text for keyword in KEYWORDS_TO_FIND) and not any(
        exclude in text for exclude in EXCLUDE_KEYWORDS)


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def select_crawler(browser, url):
    crawler_mapping = {
        "boe.es": crawl_boe,
        "juntadeandalucia": crawl_boja,
        "boa.aragon": crawl_aragon,
        "sede.asturias": crawl_asturias,
        "gobiernodecanarias": crawl_canarias,
        "bocyl": crawl_leon,
        "dogc.gencat": crawl_catalunya,
        "xunta.gal": crawl_galicia,
        "web.larioja": crawl_rioja,
        "borm": crawl_murcia,
        "bocm": crawl_madrid,
        "bon.navarra": crawl_navarra,
        "euskadi": crawl_euskadi,
        "dogv.gva": crawl_valencia
    }
    for key, func in crawler_mapping.items():
        if key in url:
            func(browser)
            break


def crawling_in_my_skin(browser):
    # Start with the main BOE and open the links for each region
    crawl_boe(browser)
    browser.get("https://boe.es/legislacion/otros_diarios_oficiales.php#boletines_autonomicos")
    links = get_links_comunidades(browser)
    for link in links:
        browser.get(link)
        select_crawler(browser, link)


def get_links_comunidades(browser):
    """
    Extracts URLs for each autonomous community's bulletin page.
    """
    xpath_template = "/html/body/div[4]/div/div/ul/li[2]/ul[{}]/li[1]/a"
    urls = []
    for i in range(1, 18):
        try:
            url = browser.find_element_by_xpath(xpath_template.format(i)).get_attribute("href")
            urls.append(url)
        except NoSuchElementException:
            continue
    return urls


def crawl_boe(browser):
    browser.get("https://boe.es")
    browser.find_element_by_link_text("Último BOE").click()
    disposiciones = browser.find_elements_by_class_name("dispo")
    for dispo in disposiciones:
        dispo_text = dispo.text.lower()
        if check_disposicion(dispo_text):
            link = dispo.find_element_by_class_name("puntoHTML").find_element_by_link_text(
                "Otros formatos").get_attribute("href")
            write_url(link)


def crawl_boja(browser):
    browser.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[1]/ol/li[1]/a").click()
    for i in range(2, 6):
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div[2]/ul/li[1]/a")))
        items = browser.find_elements_by_class_name("item")
        for item in items:
            if "educación" in item.text.lower():
                for dispo in item.find_elements_by_tag_name("div"):
                    dispo_text = dispo.find_element_by_tag_name("p").text.lower()
                    if check_disposicion(dispo_text):
                        link = dispo.find_element_by_class_name("item_html").get_attribute("href")
                        write_url(link)
        try:
            browser.find_element_by_xpath("/html/body/div[4]/div/div[2]/ol/li[" + str(i) + "]/a").click()
        except NoSuchElementException:
            continue


def crawl_aragon(browser):
    WebDriverWait(browser, 20).until(EC.frame_to_be_available_and_switch_to_it(0))
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/a/span"))).click()
    browser.switch_to.window(browser.window_handles[0])
    soup = get_soup(browser.current_url)
    disposiciones = soup.find_all("h5", {"class": "boatitulo"})
    for dispo in disposiciones:
        dispo_text = dispo.text.lower()
        if check_disposicion(dispo_text):
            link = 'http://www.boa.aragon.es' + dispo.find_next("a")["href"]
            write_url(link)


def crawl_asturias(browser):
    browser.find_element_by_xpath('//*[@id="_pa_sede_bopa_web_portlet_SedeBopaSearchDateWeb_submit"]').click()
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                 "/html/body/div[1]/div/section/div[4]/div/div/div/div/section/div/div[2]/div/div/div/div/div/fieldset/div/div/div/div/div[6]/div/div/div/a[2]")))
    soup = get_soup(browser.current_url)
    disposiciones = soup.find_all("dt")
    for dispo in disposiciones:
        link = dispo.find_next("a")["href"]
        dispo_text = dispo.get_text()
        if check_disposicion(dispo_text):
            write_url(link)


def crawl_canarias(browser):
    browser.find_element_by_css_selector("p.justificado_boc:nth-child(2) > a:nth-child(1)").click()
    soup = get_soup(browser.current_url)
    disposiciones = soup.find_all("ul")
    for dispo in disposiciones:
        dispo_text = dispo.get_text()
        for link_tag in dispo.find_all("a", title="Vista previa (Versión no oficial)"):
            link = "http://www.gobiernodecanarias.org" + link_tag.get("href")
            if check_disposicion(dispo_text):
                write_url(link)

# Repeat similar code for other crawlers by following this template.
