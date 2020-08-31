from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
os.chdir(r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs")

with open("webs") as direcciones:
    lista_raw = direcciones.readlines()  # returns a list containing each line of the documents

# formats the url list and creates a logger instance
format_direcciones(lista_raw)

"""
Here i create a new profile for Firefox to download pdfs clicking on their links
"""

binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
newpath = r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs"

mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
fp.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
fp.set_preference("pdfjs.disabled", True)


# creates new webdriver with the settings
browser = webdriver.Firefox(firefox_profile=fp)

browser.get("http://magislex.com/")
Classes.log_in(browser)
Classes.in_disposiciones(browser)

# aquí entra entra en los frames y espera a que esté disponible el botón para clickar
browser.switch_to.default_content()
browser.switch_to.frame("mainFrame")
browser.switch_to.frame("contenidoFrame")
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                             "body > form:nth-child(6) > table:nth-child(1) > "
                                                             "tbody:nth-child(1) > tr:nth-child(1) > "
                                                             "td:nth-child("
                                                             "2) > "
                                                             "input:nth-child(1)")))

# now we iterate through all urls in the list and fill the form with the info inside
for i in lista_mejor:
    # resets previous disposition
    Classes.reset_datos_disposicion()
    # opens the disposición in new tab
    browser.execute_script("window.open('" + str(i) + "');")
    # switch focus to new tab
    browser.switch_to.window(browser.window_handles[1])
    # read new one
    Classes.read_disposicion_html(i, browser)
    # closes tab
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    Classes.fill_form(Classes.datos_disposicion, browser)
    Classes.back_to_disposiciones(browser)

""" podría hacerlo para que eliminara cada url de la lista cuando la acaba de usar para así saber dónde ha fallado
"""
