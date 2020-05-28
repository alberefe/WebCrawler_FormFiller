from selenium import webdriver

"""programa logear y rellenar campos en magislex"""

# variables
usuario = "paulino"
password = "agosto"
usuario_CSS = "body > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > table:nth-child(" \
              "1) > tbody:nth-child(1) > tr:nth-child(19) > td:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) " \
              "" \
              "" \
              "> tr:nth-child(3) > td:nth-child(2) > input:nth-child(6)"
password_CSS = "body > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > table:nth-child(" \
               "1) > tbody:nth-child(1) > tr:nth-child(19) > td:nth-child(1) > table:nth-child(3) > tbody:nth-child(" \
               "1) > tr:nth-child(3) > td:nth-child(2) > input:nth-child(9)"
entrar_CSS = "body > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > table:nth-child(1) " \
             "" \
             "> tbody:nth-child(1) > tr:nth-child(19) > td:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > " \
             "tr:nth-child(3) > td:nth-child(2) > div:nth-child(11) > a:nth-child(1)"

# opens firefox and goes to magislex
driver = webdriver.Firefox()
driver.get('http://magislex.com/')

# fills user and password
usuario_fill = driver.find_element_by_css_selector(usuario_CSS)
password_fill = driver.find_element_by_css_selector(password_CSS)
entrar_button = driver.find_element_by_css_selector(entrar_CSS)
usuario_fill.send_keys('paulino')
password_fill.send_keys('agosto')
entrar_button.click()
