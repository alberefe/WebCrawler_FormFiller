from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Classes import Writer
import datetime
import Classes
import re
import datetime

fecha_regex = re.compile(r"(\d{1,2}) de ([a-z]*)([de \d{4}]*)")
match_fecha = re.search(fecha_regex,
                        "DECRETO 53/2020, de 4 de junio por el que se acuerda la implantación de las enseñanzas "
                        "conducentes a la obtención del título oficial de Grado en Fisioterapia por la Universidad "
                        "Fernando Pessoa-Canarias.")
print(match_fecha[2])
