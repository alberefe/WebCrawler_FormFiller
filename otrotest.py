from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from datetime import date
import Classes
import re
import datetime
import json
import urllib
import os
import glob
import string
import Crawler
import requests
from bs4 import BeautifulSoup





browser = webdriver.Firefox()
browser.get("http://www.boa.aragon.es/#/")

"""
arreglando aragon
"""

