from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import Classes
import os

# list that will contain the correctly formatted urls
lista_mejor = []


def format_direcciones(lista):
    """
    Formats the address list so it can be processed
    """
    global lista_mejor
    for s in lista:
        lista_mejor.append(s.rstrip())


# changes dir to the one that contains the addresses
os.chdir("C:\\Users\\DickVater\\PycharmProjects\\AutoMagislex\\direcciones")

with open("webs") as direcciones:
    lista_raw = direcciones.readlines()  # returns a list containing each line of the documents

# formats the url list and creates a logger instance
format_direcciones(lista_raw)
logger = Classes.Logger()

# entra en magislex, logea y entra en disposiciones
browser = webdriver.Firefox()
browser.get("http://magislex.com/")
logger.log_in(browser)
Classes.Writer.in_disposiciones(browser)
reader = Classes.Reader()

browser.switch_to.default_content()
browser.switch_to.frame("mainFrame")
browser.switch_to.frame("contenidoFrame")
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                             "body > form:nth-child(6) > table:nth-child(1) > "
                                                             "tbody:nth-child(1) > tr:nth-child(1) > "
                                                             "td:nth-child("
                                                             "2) > "
                                                             "input:nth-child(1)")))

# this part shoud be repeated for every url in the list
driver_disposicion = webdriver.Firefox()
driver_disposicion.get(lista_mejor[0])
reader.read_disposicion(lista_mejor[0], driver_disposicion)
driver_disposicion.quit()
Classes.Writer.fill_form(Classes.Writer.datos_disposicion, browser)
