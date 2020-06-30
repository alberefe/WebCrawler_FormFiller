from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import re
from datetime import datetime


class Logger:
    """
    Clase que logea en la web
    """

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

    def log_in(self, browser):
        """
        logs in magislex, con los atributos de la clase y los identificadores
        de cada campo/botón
        Usa la variable global driver
        """
        browser.find_element_by_css_selector(self.usuario_field_CSS).send_keys(self.usuario)
        browser.find_element_by_css_selector(self.password_field_CSS).send_keys(self.password)
        browser.find_element_by_css_selector(self.entrar_button_CSS).click()


class Writer:
    """
    Clase que rellena los formularios & uploads the files
    También vuelve a entrar al formulario cuando acaba de rellenar uno de ellos
    """

    # selectores para entrar en el menú disposiciones
    base_disposiciones_CSS = "a[href*='contenido'][href*='actunor'][target='mainFrame'] b"
    frame_get_into_Base_disposiciones = "html > frameset:nth-child(2) > frameset:nth-child(1) > frameset:nth-child(3)" \
                                        " > frame:nth-child(2)"

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
                         "palabra_clave_2": palabra_clave_2, "objeto_de_regulacion": objeto_de_regulacion,
                         "plazo": plazo,
                         "fin_vigencia": fin_vigencia, "encabezado": objeto_de_regulacion,
                         "texto_completo": texto_completo}

    @staticmethod
    def in_disposiciones(browser):
        """
        entra en disposiciones desde el menú
        """

        if browser.current_url != "http://magislex.com/admon/abon0.htm":
            browser.get("http://magislex.com/admon/abon0.htm")
        browser.switch_to.frame("mainFrame")
        browser.switch_to.frame(browser.find_element_by_css_selector(Writer.frame_get_into_Base_disposiciones))
        browser.find_element_by_css_selector(Writer.base_disposiciones_CSS).click()

    @staticmethod
    def fill_form(datos, browser):
        """
        rellena el formulario con los datos del dictionary pasado como parámetro
        :param browser: el webdriver sobre el que tiene que actuar
        :param datos: es un diccionario que contiene los datos
        """
        # Aquí va clickando en diferentes cosas y las va rellenando
        browser.switch_to.default_content()
        browser.switch_to.frame("mainFrame")
        browser.switch_to.frame("contenidoFrame")
        # wait until webpage is loaded
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                     "body > form:nth-child(6) > table:nth-child(1) > "
                                                                     "tbody:nth-child(1) > tr:nth-child(1) > "
                                                                     "td:nth-child("
                                                                     "2) > "
                                                                     "input:nth-child(1)")))

        # fills rango
        browser.find_element_by_css_selector("body > form:nth-child(6) > table:nth-child(1) > "
                                             "tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > "
                                             "input:nth-child(1)").send_keys(datos["rango"])
        # fills fecha disposicion
        browser.find_element_by_css_selector(
            "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > "
            "input:nth-child(1)").send_keys(
            datos["fecha_disposicion"])

        # selects dropdown
        select = Select(browser.find_element_by_name("Boletin"))
        select.select_by_value(datos["boletin"])

        # fills fecha de publicación
        browser.find_element_by_css_selector(
            "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(2) > "
            "input:nth-child(1)").send_keys(
            datos["fecha_publicacion"])

        # fills palabras claves
        select = Select(browser.find_element_by_name("ORClave"))
        select.select_by_visible_text(datos["palabra_clave_1"])
        select = Select(browser.find_element_by_name("ORClave2"))
        select.select_by_visible_text(datos["palabra_clave_2"])

        # fills objeto de regulación
        browser.find_element_by_css_selector(
            "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(13) > td:nth-child(2) > "
            "textarea:nth-child(1)").send_keys(
            datos["objeto_de_regulacion"])

        # fills plazo
        browser.find_element_by_css_selector(
            "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(15) > td:nth-child(2) > "
            "input:nth-child(1)").send_keys(
            datos["plazo"])

        # fills fin vigencia
        browser.find_element_by_css_selector(
            "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(19) > td:nth-child(2) > "
            "input:nth-child(1)").send_keys(
            datos["fin_vigencia"])

        # fills encabezado
        browser.find_element_by_css_selector(
            "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(25) > td:nth-child(1) > "
            "div:nth-child(1) > textarea:nth-child(1)").send_keys(
            datos["encabezado"])

        # fills texto completo
        browser.find_element_by_css_selector(
            "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(30) > td:nth-child(1) > "
            "div:nth-child(1) > textarea:nth-child(1)").send_keys(
            datos["texto_completo"])

        # click en enviar boletín
        browser.find_element_by_css_selector(
            "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(35) > td:nth-child(1) > "
            "div:nth-child(1) > input:nth-child(1)").click()

        # vuelve a la página principal y podemos invocar a in_disposiciones() para volver a empezar

        # a partir de aquí empieza por "entra en disposiciones" y vuelve a empezar


class Reader:
    """
    Reads the adresses where it has to look for the info, and reads the info
    so it can be stored in Writer.
    """

    # changes directory to the one containing the txt, opens and reads it.

    @staticmethod
    def get_rango():
        if Writer.encabezado.split(' ', 1)[0].lower() == "resolución":
            return "Resolución"
        elif Writer.encabezado.split(' ', 1)[0].lower() == "orden":
            return "Orden"
        elif Writer.encabezado.split(' ', 1)[0].lower() == "decreto":
            return "Decreto"
        elif Writer.encabezado.split(' ', 1)[0].lower() == "acuerdo":
            return "Acuerdo"
        elif (Writer.encabezado.split(' ', 1)[0].lower() == "Real") and \
                (Writer.encabezado.split(' ', 1)[1].lower() == "decreto"):
            return "Real Decreto"
        else:
            return "Anuncio"

    @staticmethod
    def mes_a_numero(mes):
        if mes.lower() == "enero":
            return "01"
        elif mes.lower() == "febrero":
            return "02"
        elif mes.lower() == "marzo":
            return "03"
        elif mes.lower() == "abril":
            return "04"
        elif mes.lower() == "mayo":
            return "05"
        elif mes.lower() == "junio":
            return "06"
        elif mes.lower() == "julio":
            return "07"
        elif mes.lower() == "agosto":
            return "08"
        elif mes.lower() == "septiembre":
            return "09"
        elif mes.lower() == "octubre":
            return "10"
        elif mes.lower() == "noviembre":
            return "11"
        elif mes.lower() == "diciembre":
            return "12"

    @staticmethod
    def get_fecha_mesletras(self, a):
        fecha_regex = re.compile(r"(\d{2}) de ([a-z]*) de (\d{4})")
        match_fecha = re.search(fecha_regex, a)
        return str(match_fecha.group(1)) + "/" + str(self.mes_a_numero(match_fecha.group(2))) \
               + "/" + match_fecha.group(3)[2:4]

    @staticmethod
    def get_palabras_clave():
        """
        saca las palabras clave a partir del objeto de regulación
        """
        if "Universidad" in Writer.objeto_de_regulacion or "Universit" in Writer.objeto_de_regulacion:
            Writer.palabra_clave_1 = "Universidad"
            if "Catedrátic" in Writer.objeto_de_regulacion:
                Writer.palabra_clave_2 = "Catedráticos"

    @staticmethod
    def fin_vigencia():
        """
        de momento es algo cutre, habrá que refactorizar para no tener que cambiarlo cada año
        :return:
        """
        if Writer.palabra_clave_2 == "Catedráticos":
            return datetime.today().strftime('%d/%m/%y')[:-1] + "1"

    def read_boe(self, browser):
        """
        reads normal BOE HTML
        """
        Writer.rango = self.get_rango()  # saca el rango según el encabezado
        Writer.objeto_de_regulacion = browser.find_element_by_class_name("documento-tit").text
        Writer.texto_completo = browser.find_element_by_id("textoxslt").text
        Writer.boletin = "Boletín Oficial del Estado"
        Writer.fecha_disposicion = self.get_fecha_mesletras(self, Writer.objeto_de_regulacion)
        Writer.fecha_publicacion = datetime.today().strftime('%d/%m/%y')
        Writer.fin_vigencia = self.fin_vigencia()

    def read_disposicion_general(self, url, browser):
        """
        Case Boletín Oficial del Estado
        """
        if "boe.es" in url:
            self.read_boe(browser)
