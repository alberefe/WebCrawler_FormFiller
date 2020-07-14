from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Classes import Writer
import datetime
import Classes
import re
import datetime
import Classes
import json
import urllib
import os
import glob

logger = Classes.Logger()

""" para comprobar si el elemento existe, hay que buscar con xpath si hay algo acabado en img o table y
si exception not found, entonces continuar normalmente. Si no, hay exception, descargar pdf y añadirlo al diccionario
 
"""

driver = webdriver.Firefox()
driver.get(
    "http://www.boa.aragon.es/cgi-bin/EBOA/BRSCGI?CMD=VERDOC&BASE=BOLE&PIECE=BOLE&DOCS=1-34&DOCR=1&SEC=FIRMA&RNG=200"
    "&SEPARADOR=&&PUBL=20200713")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                             r"#pdf11BRBOLE100279267\ \ \ \ \ \ "))).click()
