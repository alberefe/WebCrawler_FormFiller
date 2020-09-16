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

browser.get("https://sede.asturias.es/portal/site/Asturias/menuitem.048b5a85ccf2cf40a9be6aff100000f7/?vgnextoid=c0c756a575acd010VgnVCM100000bb030a0aRCRD&i18n.http.lang=es&calendarioPqBopa=true")
Crawler.crawling_in_my_skin(browser)


""""
Hay que hacer que abra y cierre las pestañas adecuadamente los crawlers qque tenog hechos
"""
