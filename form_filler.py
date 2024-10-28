"""
This file contains the logic for filling out forms and uploading PDFs for 'disposiciones'.
"""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import os
import glob
import re


class Disposicion:
    """
    A class to manage data for 'disposiciones' and perform necessary form filling and PDF uploading actions
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.data = {
            "rango": "",
            "fecha_disposicion": "",
            "boletin": "",
            "fecha_publicacion": "",
            "palabra_clave_1": "",
            "palabra_clave_2": "",
            "objeto_de_regulacion": "",
            "plazo": "",
            "fin_vigencia": "",
            "encabezado": "",
            "texto_completo": "",
            "pdf": False
        }

    def update_from_text(self, obj_regulacion_text):
        self.data["encabezado"] = self.data["objeto_de_regulacion"] = obj_regulacion_text
        self.data["rango"] = get_rango(obj_regulacion_text)
        self.data["fecha_disposicion"] = get_fecha_mesletras(obj_regulacion_text)
        self.data["fecha_publicacion"] = datetime.today().strftime('%d/%m/%y')
        self.data["fin_vigencia"] = fin_vigencia(self.data["palabra_clave_2"])
        get_palabras_clave(self.data)


disposicion = Disposicion()


def get_rango(text):
    rangos = {"resolución": "Resolución", "orden": "Orden", "decreto": "Decreto", "acuerdo": "Acuerdo",
              "Real": "Real Decreto"}
    first_word = text.split(' ', 1)[0].lower()
    return rangos.get(first_word, "Anuncio")


def get_fecha_mesletras(texto):
    meses = {"enero": "01", "febrero": "02", "marzo": "03", "abril": "04", "mayo": "05", "junio": "06", "julio": "07",
             "agosto": "08", "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"}
    fecha_regex = re.compile(r"(\d{1,2}) de ([a-z]*)([de \d{4}]*)")
    match_fecha = re.search(fecha_regex, texto)
    if match_fecha:
        day = match_fecha[1].zfill(2)
        month = meses.get(match_fecha[2], "01")
        year = str(datetime.now().year)[-2:] if not match_fecha[3] else match_fecha[3][-2:]
        return f"{day}/{month}/{year}"
    return datetime.today().strftime('%d/%m/%y')


def fin_vigencia(palabra_clave_2):
    if palabra_clave_2 == "Catedráticos":
        return datetime.today().strftime('%d/%m/%y')[:-1] + "1"
    return ""


def get_pdf_name():
    list_of_files = glob.glob(r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\*")
    return max(list_of_files, key=os.path.getctime) if list_of_files else None


def click_and_fill(browser, css_selector, text):
    element = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    element.clear()
    element.send_keys(text)


def read_and_process(browser, selectors, pdf_check_func, pdf_click_selector, boletin_name):
    """Handles the general reading and PDF check and click logic for different boletins"""
    disposicion.update_from_text(browser.find_element_by_css_selector(selectors["heading"]).text)
    disposicion.data["texto_completo"] = browser.find_element_by_css_selector(selectors["content"]).text[:60000]

    if len(disposicion.data["texto_completo"]) > 60000 or pdf_check_func(browser):
        disposicion.data["pdf"] = True
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, pdf_click_selector))).click()

    disposicion.data["boletin"] = boletin_name
