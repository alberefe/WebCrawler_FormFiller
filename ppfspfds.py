from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import datetime
import Classes
import re
import datetime
import json
import urllib
import os
import glob
import string
import Crawler

palabras_buscar_disposiciones = ["universidad", "formación profesional", "educación", "educativo", "docente", "idiomas",
                                 "enseñanza", "concierto educativo", "conciertos educativos", "educación infantil",
                                 "educación secundaria", "bachillerato", "erasmus", "profesor", "catedrático", "alumn"]

browser = webdriver.Firefox()

"""
Crawler que busca las disposiones del BOJA
"""

browser.get("https://www.juntadeandalucia.es/eboja/2020/168/s1.html")
# browser.find_element_by_link_text("Disposiciones generales").click()

WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                 "/html/body/div[4]/div/div[1]/div/div[1]/div[1]/ul[2]/li/a")))

items = browser.find_elements_by_class_name("item")


for item in items:
    try:
        item.find_element_by_tag_name("h3")
        if "educación" in item.find_element_by_tag_name("h3").text.lower():
            with open(r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt",
                      "a") as urls:
                for dispo in item.find_elements_by_tag_name("div"):
                    dispo_low = dispo.find_element_by_tag_name("p").text.lower()
                    for palabra in palabras_buscar_disposiciones:
                        if palabra in dispo_low \
                                and "extravío" not in dispo_low \
                                and "anuncio de formalización" not in dispo_low \
                                and "personal de administración y servicios" not in dispo_low \
                                and "libre designación" not in dispo_low:
                            link = dispo.find_element_by_class_name("item_html").get_attribute("href")
                            print(link)
                            urls.write(link)
                            break
    except NoSuchElementException:
        continue



"""
Esto funciona para andalucía, ahora hay que hacer que visite las tres sencciones que hay en el boja y repita el mismo 
proceso
"""
