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
reader = Classes.Reader()

fecha_regex = re.compile(r"(\d{1,2}) de ([a-z]*)([de \d{4}]*)")
match_fecha = re.search(fecha_regex,
                        "Orden de 25 de febrero de 2020, de la Consejería de Educación y Cultura, por la que se "
                        "aprueba el cambio de denominación específica del Colegio de Educación Infantil y Primaria "
                        "“Santo Domingo y San Miguel” de Mula, código 30004607 a “Florentino Bayona”.")
print(match_fecha[3])
