from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

"""programa logear y rellenar campos en magislex"""

# login variables
usuario = "paulino"
password = "agosto"
usuario_field_CSS = "body > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > " \
                    "table:nth-child(" \
                    "1) > tbody:nth-child(1) > tr:nth-child(19) > td:nth-child(1) > table:nth-child(3) > " \
                    "tbody:nth-child(1)" \
                    " > tr:nth-child(3) > td:nth-child(2) > input:nth-child(6)"
password_field_CSS = "body > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > " \
                     "table:nth-child(" \
                     "1) > tbody:nth-child(1) > tr:nth-child(19) > td:nth-child(1) > table:nth-child(3) > " \
                     "tbody:nth-child(" \
                     "1) > tr:nth-child(3) > td:nth-child(2) > input:nth-child(9)"
entrar_button_CSS = "body > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > " \
                    "table:nth-child(1)" \
                    " > tbody:nth-child(1) > tr:nth-child(19) > td:nth-child(1) > table:nth-child(3) > " \
                    "tbody:nth-child(1) > " \
                    "tr:nth-child(3) > td:nth-child(2) > div:nth-child(11) > a:nth-child(1)"

#  main menu variables
base_disposiciones_CSS = "a[href*='contenido'][href*='actunor'][target='mainFrame'] b"
frame_get_into_Base_disposiciones = "html > frameset:nth-child(2) > frameset:nth-child(1) > frameset:nth-child(3) > " \
                                    "frame:nth-child(2)"

# filling fields Base de datos de Disposiciones Vigentes
rango = ""
fecha_disposicion = ""
boletin = ""
fecha_publicacion = ""  # maybe as an argument when executing the program
palabra_clave_1 = ""
palabra_clave_2 = ""
objeto_de_regulacion = ""
plazo = ""
fin_vigencia = ""
encabezado = objeto_de_regulacion
texto_completo = ""

# esto es el diccionario que se pasa como parámetro a la función que rellena los datos
datos_disposicion = {"rango": rango, "fecha_disposicion": fecha_disposicion, "boletin": boletin,
                     "fecha_publicacion": fecha_publicacion, "palabra_clave_1": palabra_clave_1,
                     "palabra_clave_2": palabra_clave_2, "objeto_de_regulacion": objeto_de_regulacion, "plazo": plazo,
                     "fin_vigencia": fin_vigencia, "encabezado": objeto_de_regulacion, "texto_completo": texto_completo}

# opens firefox and goes to magislex
driver = webdriver.Firefox()
driver.get('http://magislex.com/')


def log_in():
    """
    logs in magislex
    """
    usuario_fill = driver.find_element_by_css_selector(usuario_field_CSS)
    password_fill = driver.find_element_by_css_selector(password_field_CSS)
    entrar_button = driver.find_element_by_css_selector(entrar_button_CSS)
    usuario_fill.send_keys('paulino')
    password_fill.send_keys('agosto')
    entrar_button.click()


def in_disposiciones():
    """
    entra en disposiciones
    """
    driver.switch_to.frame("mainFrame")
    driver.switch_to.frame(driver.find_element_by_css_selector(frame_get_into_Base_disposiciones))
    driver.find_element_by_css_selector(base_disposiciones_CSS).click()


def fill_form(datos):
    """
    rellena el formulario con los datos del dictionary pasado como parámetro
    :param datos: es un diccionario que contiene los datos
    """
    # Aquí va clickando en diferentes cosas y las va rellenando
    driver.switch_to.default_content()
    driver.switch_to.frame("mainFrame")
    driver.switch_to.frame("contenidoFrame")
    # wait until webpage is loaded
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                "body > form:nth-child(6) > table:nth-child(1) > "
                                                                "tbody:nth-child(1) > tr:nth-child(1) > td:nth-child("
                                                                "2) > "
                                                                "input:nth-child(1)")))

    # fills rango
    driver.find_element_by_css_selector("body > form:nth-child(6) > table:nth-child(1) > "
                                        "tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > "
                                        "input:nth-child(1)").send_keys(datos["rango"])
    # fills fecha disposicion
    driver.find_element_by_css_selector(
        "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > "
        "input:nth-child(1)").send_keys(
        datos["fecha_disposicion"])

    # selects dropdown
    select = Select(driver.find_element_by_name("Boletin"))
    select.select_by_value(datos["boletin"])

    # fills fecha de publicación
    driver.find_element_by_css_selector(
        "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(2) > "
        "input:nth-child(1)").send_keys(
        datos["fecha_publicacion"])

    # fills palabras claves
    select = Select(driver.find_element_by_name("ORClave"))
    select.select_by_visible_text(datos["palabra_clave_1"])
    select = Select(driver.find_element_by_name("ORClave2"))
    select.select_by_visible_text(datos["palabra_clave_2"])

    # fills objeto de regulación
    driver.find_element_by_css_selector(
        "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(13) > td:nth-child(2) > "
        "textarea:nth-child(1)").send_keys(
        datos["objeto_de_regulacion"])

    # fills plazo
    driver.find_element_by_css_selector(
        "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(15) > td:nth-child(2) > "
        "input:nth-child(1)").send_keys(
        datos["plazo"])

    # fills fin vigencia
    driver.find_element_by_css_selector(
        "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(19) > td:nth-child(2) > "
        "input:nth-child(1)").send_keys(
        datos["fin_vigencia"])

    # fills encabezado
    driver.find_element_by_css_selector(
        "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(25) > td:nth-child(1) > "
        "div:nth-child(1) > textarea:nth-child(1)").send_keys(
        datos["encabezado"])

    # fills texto completo
    driver.find_element_by_css_selector(
        "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(30) > td:nth-child(1) > "
        "div:nth-child(1) > textarea:nth-child(1)").send_keys(
        datos["texto_completo"])

    driver.find_element_by_css_selector(
        "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(35) > td:nth-child(1) > "
        "div:nth-child(1) > input:nth-child(1)").click()

    driver.get("http://magislex.com/admon/abon0.htm")
    # a partir de aquí empieza por "entra en disposiciones" y vuelve a empezar


log_in()
in_disposiciones()
fill_form(datos_disposicion)
