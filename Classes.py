from selenium.common.exceptions import NoSuchElementException
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
    It's a class but everything is static
    """

    # selectores para entrar en el menú disposiciones
    base_disposiciones_CSS = "a[href*='contenido'][href*='actunor'][target='mainFrame'] b"
    frame_get_into_Base_disposiciones = "html > frameset:nth-child(2) > frameset:nth-child(1) > frameset:nth-child(3)" \
                                        " > frame:nth-child(2)"

    # esto es el diccionario que se pasa como parámetro a la función que rellena los datos
    datos_disposicion = {"rango": "", "fecha_disposicion": "", "boletin": "",
                         "fecha_publicacion": "", "palabra_clave_1": "",
                         "palabra_clave_2": "", "objeto_de_regulacion": "",
                         "plazo": "",
                         "fin_vigencia": "", "encabezado": "",
                         "texto_completo": ""}

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
        if Writer.datos_disposicion["fin_vigencia"]:
            browser.find_element_by_css_selector(
                "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(19) > "
                "td:nth-child(2) > "
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
        rangos = {"resolución": "Resolución", "orden": "Orden", "decreto": "Decreto", "acuerdo": "Acuerdo",
                  "Real": "Real Decreto"}

        for rang in rangos.keys():
            if rang == Writer.datos_disposicion["objeto_de_regulacion"].split(' ', 1)[0].lower():
                return rangos[rang]

        # return if doesn't find anything
        return "Anuncio"

    @staticmethod
    def mes_a_numero(mes):
        meses = {"enero": "01", "febrero": "02", "marzo": "03", "abril": "04", "mayo": "05", "junio": "06",
                 "julio": "07", "agosto": "08", "septiembre": "09", "octubre": "10", "noviembre": "11",
                 "diciembre": "12"}
        for m in meses.keys():
            if mes == m:
                return meses[m]

    def get_fecha_mesletras(self, a):
        fecha_regex = re.compile(r"(\d{1,2}) de ([a-z]*)([de \d{4}]?)")
        match_fecha = re.search(fecha_regex, a)
        if match_fecha[3]:
            return str(match_fecha.group(1)) + "/" + str(self.mes_a_numero(match_fecha.group(2))) \
                   + "/" + match_fecha.group[3][-2:]
        else:
            return str(match_fecha.group(1)) + "/" + str(self.mes_a_numero(match_fecha.group(2))) \
                   + "/" + str(datetime.now().year)[-2:]


    @staticmethod
    def get_palabras_clave():
        """
        saca las palabras clave a partir del objeto de regulación
        """
        palabras = {"Universidad": "Universidad", "Universit": "Universidad", "subvenci": "Becas y subvenciones",
                    "Subvenci": "Becas y subvenciones", "ayudas": "Becas y subvenciones",
                    "beca": "Becas y subvenciones", "Ayudas": "Becas y subvenciones", "Beca": "Becas y subvenciones",
                    "Premio": "Becas y subvenciones", "Formación Profesional": "Formación Profesional",
                    "centro": "Centros", "Centro": "Centros", "escuela": "Centros", "unidades escolares": "Centros",
                    "nueva denominación específica": "Centros", "puestos de trabajo docentes": "Cuerpos docentes",
                    "funcionarias de carrera": "Cuerpos docente", "funcionarios de carrera": "Cuerpos docentes",
                    "bachillerato": "Bachillerato", "Bachillerato": "Bachillerato", "idiomas": "Idiomas",
                    "inglés": "Idiomas", "concurso de traslados": "Concurso de traslados", "concierto": "Conciertos",
                    "interin": "Interinos", "plantilla": "Cuerpos docentes", "Cuerpo de Maestros": "Cuerpos docentes",
                    "infantil": "Educación Infantil", "Infantil": "Educación Infantil",
                    "secundaria": "Enseñanza Obligatoria", "Secundaria": "Enseñanza Obligatoria"}
        palabras_uni = {"Catedrátic": "Catedráticos", "Profesor": "Catedráticos", "plan de estudios": "Centros",
                        "concurso": "Oposiciones", "presupuesto": "Presupuesto", "subvenci": "Becas y subvenciones",
                        "Subvenci": "Becas y subvenciones", "ayudas": "Becas y subvenciones",
                        "beca": "Becas y subvenciones", "Ayudas": "Becas y subvenciones",
                        "Beca": "Becas y subvenciones",
                        "Premio": "Becas y subvenciones"}

        for pal in palabras.keys():
            if pal in Writer.datos_disposicion["objeto_de_regulacion"]:
                Writer.datos_disposicion["palabra_clave_1"] = palabras[pal]
                break

        if Writer.datos_disposicion["palabra_clave_1"] == "Universidad":
            for pal_uni in palabras_uni.keys():
                if pal_uni in Writer.datos_disposicion["objeto_de_regulacion"]:
                    Writer.datos_disposicion["palabra_clave_2"] = palabras_uni[pal_uni]
                    break
            else:
                Writer.datos_disposicion["palabra_clave_2"] = "Catedráticos"

    @staticmethod
    def fin_vigencia():
        """
        de momento es algo cutre, habrá que refactorizar para no tener que cambiarlo cada año
        :return:
        """
        if Writer.datos_disposicion["palabra_clave_2"] == "Catedráticos":
            return datetime.today().strftime('%d/%m/%y')[:-1] + "1"

    def process_disposition(self):
        """
        processes the text of the disposition to get the neccessary info
        """
        Writer.datos_disposicion["encabezado"] = Writer.datos_disposicion["objeto_de_regulacion"]
        Writer.datos_disposicion["rango"] = self.get_rango()
        Writer.datos_disposicion["fecha_disposicion"] = self.get_fecha_mesletras(Writer.datos_disposicion[
                                                                                     "objeto_de_regulacion"])
        Writer.datos_disposicion["fecha_publicacion"] = datetime.today().strftime('%d/%m/%y')
        Writer.datos_disposicion["fin_vigencia"] = self.fin_vigencia()
        self.get_palabras_clave()

    def read_boe(self, browser):
        """
        reads normal BOE HTML
        """
        # first it has to change to a container
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_class_name("documento-tit").text
        Writer.datos_disposicion["texto_completo"] = browser.find_element_by_id("textoxslt").text
        Writer.datos_disposicion["boletin"] = "Boletín Oficial del Estado"
        self.process_disposition()

    @staticmethod
    def sacar_texto_boja(driver):
        s = ""
        try:
            i = 1
            t = True
            while t:
                s += driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/p[" + str(i) + "]").text + "\n"
                i += 1
        except NoSuchElementException:
            pass

        return s

    def read_boja(self, browser):
        """
        reads Boletín Andalucía
        """
        # first it has to change to a container
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_xpath(
            "/html/body/div[4]/div/div[1]/div/div[1]/h4").text
        Writer.datos_disposicion["texto_completo"] = self.sacar_texto_boja(browser)
        Writer.datos_disposicion["boletin"] = "Boletín Oficial de la Junta de Andalucía"
        self.process_disposition()

    @staticmethod
    def sacar_texto_aragon(browser):
        s = ""
        try:

            i = 1
            t = True
            while t:
                s += browser.find_element_by_xpath("/html/body/div/div/section/div/div/p[" + str(i) + "]" + "\n").text
                i += 1
        except NoSuchElementException:
            pass
        return s

    def read_aragon(self, browser):
        """
        read boletín de aragón
        :param: the webdriver in use at the moment
        """
        # lee objeto de regulación y texto
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_xpath(
            "/html/body/div/div/section/div/div/div[2]/h3/span[2]").text
        Writer.datos_disposicion["texto_completo"] = self.sacar_texto_aragon(browser)
        Writer.datos_disposicion["boletin"] = "Boletín Oficial de Aragón"
        self.process_disposition()

    @staticmethod
    def sacar_texto_asturias(browser):
        s = ""
        try:

            i = 2  # i starts at 2 because the first <p> is the "objeto de regulación"
            t = True
            while t:
                s += browser.find_element_by_xpath(
                    "/html/body/div[2]/div[2]/div/div/div/div[3]/div/div[3]/div/p[" + str(i) + "]" + "\n").text
                i += 1
        except NoSuchElementException:
            pass
        return s

    def read_asturias(self, browser):
        """
        read boletín de asturias
        :param: the webdriver in use at the moment
        """
        # lee objeto de regulación y texto
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div/div/div/div[3]/div/div[3]/div/p[1]").text
        Writer.datos_disposicion["texto_completo"] = self.sacar_texto_asturias(browser)
        Writer.datos_disposicion["boletin"] = "Boletín Oficial del Principado de Asturias"
        self.process_disposition()

    @staticmethod
    def sacar_objeto_regulacion_canarias(browser):
        """
        extracts the heading of boe canarias
        :return:
        """
        pattern = re.compile(r"\d* página")
        s = browser.find_element_by_xpath("/html/body/div/div[4]/div[2]/div/h3").text[
            5:re.search(pattern, browser.find_element_by_xpath("/html/body/div/div[4]/div[2]/div/h3").text).start()]
        return s

    @staticmethod
    def sacar_texto_canarias(browser):
        s = ""
        try:

            i = 1  # i starts at 2 because the first <p> is the "objeto de regulación"
            t = True
            while t:
                s += browser.find_element_by_xpath("/html/body/div/div[4]/div[2]/div/p[" + str(i) + "]").text + "\n"
                i += 1
        except NoSuchElementException:
            pass
        return s

    def read_canarias(self, browser):
        Writer.datos_disposicion["objeto_de_regulacion"] = self.sacar_objeto_regulacion_canarias(browser)
        Writer.datos_disposicion["texto_completo"] = self.sacar_texto_canarias(browser)
        Writer.datos_disposicion["boletin"] = "Boletín Oficial de Canarias"
        self.process_disposition()

    def read_disposicion(self, url, browser):
        """
        Case Boletín Oficial del Estado
        """
        if "boe.es" in url:
            self.read_boe(browser)
        if "juntadeandalucia" in url:
            self.read_boja(browser)
        if "boa.aragon" in url:
            self.read_aragon(browser)
        if "sede.asturias" in url:
            self.read_asturias(browser)
        if "gobiernodecanarias" in url:
            self.read_canarias(browser)


""" puedo asignar a los método del otro módulo el nombre de una variable para poder usarlo sin que esté tan petado de 
cosas"""
