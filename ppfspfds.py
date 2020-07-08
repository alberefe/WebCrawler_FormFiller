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
import Classes

driver = webdriver.Firefox()
reader = Classes.Reader()
logger = Classes.Logger()

driver.get("http://magislex.com/")

logger.log_in(driver)

Writer.in_disposiciones(driver)

driver.switch_to.default_content()
driver.switch_to.frame("mainFrame")
driver.switch_to.frame(
    driver.find_element_by_xpath("/html/frameset/frameset/frame[1]"))
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                            "body > table:nth-child(1) > tbody:nth-child(1) > "
                                                            "tr:nth-child(4) > td:nth-child(1) > a:nth-child(1)")))
driver.find_element_by_css_selector(
    "body > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > a:nth-child(1)").click()
