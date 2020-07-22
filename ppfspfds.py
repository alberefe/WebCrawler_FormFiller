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
reader.read_disposicion_html(i, browser)
print(Classes.Writer.datos_disposicion)
