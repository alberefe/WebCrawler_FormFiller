from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from datetime import date
import Classes
import re
import datetime
import json
import urllib
import os
import glob
import string
import Crawler
import requests
from bs4 import BeautifulSoup

browser = webdriver.Firefox()
browser.get("https://dogc.gencat.cat/es/index.html?newLang=es_ES&language=es_ES")
"""
crawler catalunya
"""

# entra en la página principal de las disposiciones
try:
    browser.find_element_by_css_selector(
        "#sumari > ul:nth-child(2) > li:nth-child(1) > form:nth-child(2) > a:nth-child(1)").click()
except NoSuchElementException:
    try:
        browser.find_element_by_css_selector(
            "#sumari > ul:nth-child(2) > li:nth-child(2) > form:nth-child(2) > a:nth-child(1)").click()
    except NoSuchElementException:
        print("no hay disposiciones hoy, aquí hay que poner un return")

WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[2]/div/div/div/div[4]/div[4]/div[1]/div/div/div[2]/ul/li[2]/span/a[2]")))

# crea el bs4 object
url = browser.current_url
soup = BeautifulSoup(requests.get(url).content, "html.parser")

lista_disposiciones = soup.find_all("p", {"class": "separador negreta"})

with open(
        r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt"
        , "a") as urls:
    for disposicion in lista_disposiciones:
        # aquí selecciona sólo los links que llevan al html
        link = disposicion.find_next("a", title="Versión HTML")["href"]
        print(link)
        text = disposicion.get_text()
        print(text)
        # if Crawler.check_disposicion(Crawler.palabras_buscar_disposiciones, text):
        #    urls.write(str(link_url) + "\n")
