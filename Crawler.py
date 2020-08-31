from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

"""
This file contains the functions that look for the documents that interest us
"""

# these are the words we are looking for in the text of the dispositions
palabras_buscar_disposiciones = ["universidad", "formación profesional", "educación", "educativo", "docente", "idiomas",
                                 "enseñanza", "concierto educativo", "conciertos educativos", "educación infantil",
                                 "educación secundaria", "bachillerato", "erasmus", "profesor", "catedrático", "alumn"]


def crawl_boe(browser):
    """
    Crawler que busca las disposiciones del BOE
    """
    browser.get("https://boe.es")
    browser.find_element_by_link_text("Último BOE").click()
    disposiciones = browser.find_elements_by_class_name("dispo")

    with open(r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt",
              "a") as urls:
        for dispo in disposiciones:
            dispo_low = dispo.text.lower()
            for palabra in palabras_buscar_disposiciones:
                if palabra in dispo_low \
                        and "extravío" not in dispo_low \
                        and "anuncio de formalización" not in dispo_low \
                        and "personal de administración y servicios" not in dispo_low \
                        and "libre designación" not in dispo_low:
                    link = dispo.find_element_by_class_name("puntoHTML").find_element_by_link_text(
                        "Otros formatos").get_attribute("href") + "\n"
                    urls.write(link)
                    break


def crawl_boja(browser):
    """
    Crawler que busca las disposiones del BOJA
    """
    browser.get("https://www.juntadeandalucia.es/eboja")
    browser.find_element_by_link_text("Disposiciones generales").click()
