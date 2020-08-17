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

c = Classes.Reader()

print(c.get_fecha_mesletras(
    "ORDEN 1829/2020, de 4 de agosto, del Consejero de Educación y Juventud, por la que se establece la autorización y "
    "supresión de enseñanzas en institutos de educación secundaria y centros de educación de personas adultas, a partir"
    " del curso 2020-2021."))
print(c.get_fecha_mesletras(
    "ORDEN 1829/2020, de 4 de agosto, del Consejero de Educación y Juventud, por la que se establece la autorización y "
    "supresión de enseñanzas en institutos de educación secundaria y centros de educación de personas adultas, a partir"
    " del curso 2020-2021."))
