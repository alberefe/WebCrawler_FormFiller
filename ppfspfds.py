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

browser= webdriver.Firefox()
logger = Classes.Logger()
reader = Classes.Reader()
browser.get("https://boe.es/diario_boe/txt.php?id=BOE-A-2020-8472")
reader.read_disposicion_html("https://boe.es/diario_boe/txt.php?id=BOE-A-2020-8472", browser)
print(Classes.Writer.datos_disposicion)
