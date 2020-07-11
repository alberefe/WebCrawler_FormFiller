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

reader = Classes.Reader()
logger = Classes.Logger()



for values in Writer.datos_disposicion.values():
    print(values)

""" para comprobar si el elemento existe, hay que buscar con xpath si hay algo acabado en img o table y
si exception not found, entonces continuar normalmente. Si no, hay exception, descargar pdf y añadirlo al diccionario
 
"""