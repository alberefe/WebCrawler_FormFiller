import glob

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import re
from datetime import datetime
import os


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
                         "texto_completo": "", "pdf": False}

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
    def back_to_disposiciones(browser):
        """
        Goes back to disposiciones after filling the form
        """
        browser.switch_to.default_content()
        browser.switch_to.frame("mainFrame")
        browser.switch_to.frame(
            browser.find_element_by_xpath("/html/frameset/frameset/frame[1]"))
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                     "body > table:nth-child(1) > tbody:nth-child(1) > "
                                                                     "tr:nth-child(4) > td:nth-child(1) > a:nth-child("
                                                                     "1)")))
        browser.find_element_by_css_selector(
            "body > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > a:nth-child("
            "1)").click()

    @staticmethod
    def get_pdf_name():
        """
        returns the path of the pdf to be uploaded by returning the last saved file
        """
        list_of_files = glob.glob(r"C:\Users\DickVater\PycharmProjects\AutoMagislex\urls&pdfs\*")
        latest_file = max(list_of_files, key=os.path.getctime)
        return str(latest_file)

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

        # uploads the pdf
        if Writer.datos_disposicion["pdf"]:
            browser.find_element_by_name("pdf").send_keys(
                Writer.get_pdf_name())

        # click en enviar boletín
        browser.find_element_by_css_selector(
            "body > form:nth-child(6) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(35) > td:nth-child(1) > "
            "div:nth-child(1) > input:nth-child(1)").click()

    # vuelve a la página principal y podemos invocar a in_disposiciones() para volver a empezar

    @staticmethod
    def reset_datos_disposicion():
        """
         resets the values in the dictionary so we prevent
         errors in the next disposition
        """
        for key in Writer.datos_disposicion.keys():
            if key == "pdf":
                Writer.datos_disposicion[key] = False
            else:
                Writer.datos_disposicion[key] = ""


class Reader:
    """
    Reads the adresses where it has to look for the info, and reads the info
    so it can be stored in Writer.
    """

    # changes directory to the one containing the txt, opens and reads it.

    @staticmethod
    def get_rango():
        rangos = {"resolución": "Resolución", "orden": "Orden", "decreto": "Decreto", "acuerdo": "Acuerdo",
                  "Real": "Real Decreto", "Acuerdo": "Acuerdo"}

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

    def get_fecha_mesletras(self, texto):
        fecha_regex = re.compile(r"(\d{1,2}) de ([a-z]*)([de \d{4}]*)")
        match_fecha = re.search(fecha_regex, texto)
        try:
            return str(match_fecha[1].zfill(2)) + "/" + str(self.mes_a_numero(match_fecha[2])) \
                   + "/" + str(match_fecha[3].rstrip()[-2:])
        except TypeError:
            # no está tratando la excepción adecuadamente
            return str(match_fecha[1]) + "/" + str(self.mes_a_numero(match_fecha[2])) \
                   + "/" + str(datetime.now().year)[-2:]

    @staticmethod
    def get_palabras_clave():
        """
        saca las palabras clave a partir del objeto de regulación
        """
        palabras = {"Universidad": "Universidad", "Universitat": "Universidad", "universidad": "Universidad",
                    "Universit": "Universidad", "Técnico Superior": "Formación Profesional",
                    "subvenci": "Becas y subvenciones", "Subvenci": "Becas y subvenciones",
                    "ayudas": "Becas y subvenciones", "beca": "Becas y subvenciones", "Ayudas": "Becas y subvenciones",
                    "Beca": "Becas y subvenciones", "Premio": "Becas y subvenciones",
                    "procedimiento selectivo": "Cuerpos docentes", "profesorado": "Cuerpos docentes",
                    "Formación Profesional": "Formación Profesional", "Oferta de Empleo": "Puestos de trabajo",
                    "centro": "Centros", "Centro": "Centros", "escuela": "Centros", "unidades escolares": "Centros",
                    "nueva denominación específica": "Centros", "puestos de trabajo docentes": "Cuerpos docentes",
                    "funcionarias de carrera": "Cuerpos docente", "funcionarios de carrera": "Cuerpos docentes",
                    "admisión": "Centros", "colegio": "Centros", "Erasmus": "Becas y subvenciones",
                    "bachillerato": "Bachillerato", "Bachillerato": "Bachillerato", "idiomas": "Idiomas",
                    "inglés": "Idiomas", "concurso de traslados": "Concurso de traslados",
                    "traslados": "Concurso de traslados", "concierto": "Conciertos",
                    "interin": "Interinos", "plantilla": "Cuerpos docentes", "Cuerpo de Maestros": "Cuerpos docentes",
                    "infantil": "Educación Infantil", "Infantil": "Educación Infantil", "lingüístic": "Idiomas",
                    "secundaria": "Enseñanza Obligatoria", "Secundaria": "Enseñanza Obligatoria",
                    "plan de estudios": "Universidad"}

        palabras_uni = {"Catedrátic": "Catedráticos", "Profesor": "Catedráticos", "provisión": "Catedráticos",
                        "profesor": "Catedráticos", "titular": "Catedráticos", "plan de estudios": "Centros",
                        "pruebas selectivas": "Oposiciones", "Oferta de Empleo": "Puestos de trabajo",
                        "concurso": "Oposiciones", "presupuesto": "Presupuesto", "subvenci": "Becas y subvenciones",
                        "Subvenci": "Becas y subvenciones", "ayudas": "Becas y subvenciones",
                        "beca": "Becas y subvenciones", "Ayudas": "Becas y subvenciones",
                        "Beca": "Becas y subvenciones", "oferta pública": "Oposiciones", "acceso": "Alumnos",
                        "Premio": "Becas y subvenciones", "profesorado agregado": "Catedráticos",
                        "modificación": "Centros", "personal docente": "Oposiciones",
                        "procedimientos de matrícula": "Alumnos", "Convenio": "Centros", "convenio": "Centros"}

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

        if Writer.datos_disposicion["palabra_clave_1"] == "":
            Writer.datos_disposicion["palabra_clave_1"] = "Centros"

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

    @staticmethod
    def pdf_boe(browser):
        try:
            browser.find_element_by_id("textoxslt").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            try:
                browser.find_element_by_id("textoxslt").find_element_by_tag_name("img")
                return True
            except NoSuchElementException:
                return False

    def read_boe_html(self, browser):
        """
        reads normal BOE HTML
        """
        # first it has to change to a container
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                         "documento-tit")))
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_class_name("documento-tit").text
        Writer.datos_disposicion["texto_completo"] = browser.find_element_by_id("textoxslt").text

        # now checks if the len of the body is too long or there are tables or img and downloads pdf in case
        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_boe(browser):
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                         "/html/body/div[4]/div/div[1]/div/ul/li["
                                                                         "2]/a"))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        Writer.datos_disposicion["boletin"] = "Boletín Oficial del Estado"
        self.process_disposition()

    @staticmethod
    def sacar_texto_boja_html(driver):
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

    @staticmethod
    def pdf_boja(browser):
        try:
            browser.find_element_by_id("cuerpo").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            try:
                browser.find_element_by_id("cuerpo").find_element_by_tag_name("img")
                return True
            except NoSuchElementException:
                return False

    def read_boja_html(self, browser):
        """
        reads Boletín Andalucía
        """
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                         "/html/body/div[4]/div/div[1]/div/div[1]/h4")))
        # first it has to change to a container
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_xpath(
            "/html/body/div[4]/div/div[1]/div/div[1]/h4").text
        Writer.datos_disposicion["texto_completo"] = self.sacar_texto_boja_html(browser)

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_boja(browser):
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                         "/html/body/div[4]/div/div[1]/div/a["
                                                                         "2]"))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        Writer.datos_disposicion["boletin"] = "Boletín Oficial de la Junta de Andalucía"
        self.process_disposition()

    @staticmethod
    def sacar_texto_aragon_html(browser):
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

    @staticmethod
    def pdf_aragon(browser):
        """
        in aragon there are no images, for what i know
        :param browser:
        :return:
        """
        try:
            browser.find_element_by_id("leelo").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            return False

    def read_aragon_html(self, browser):
        """
        read boletín de aragón
        :param: the webdriver in use at the moment
        """
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/section/div/div/div[2]/h3/span[2]")))
        # lee objeto de regulación y texto
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_xpath(
            "/html/body/div/div/section/div/div/div[2]/h3/span[2]").text
        Writer.datos_disposicion["texto_completo"] = self.sacar_texto_aragon_html(browser)

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_boja(browser):
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         r"#pdf11BRBOLE100279267\ \ \ \ \ \ "))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        Writer.datos_disposicion["boletin"] = "Boletín Oficial de Aragón"

        self.process_disposition()

    @staticmethod
    def sacar_texto_asturias_html(browser):
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

    @staticmethod
    def pdf_asturias(browser):
        """
        in aragon there are no images, for what i know
        :param browser:
        :return:
        """
        if "Ver anuncio en PDF para consultar la tabla" in Writer.datos_disposicion["texto_completo"]:
            return True

        try:
            browser.find_element_by_id("bopa-articulo").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            pass

        try:
            browser.find_element_by_id("bopa-articulo").find_element_by_tag_name("img")
            return True
        except NoSuchElementException:
            return False

    def read_asturias_html(self, browser):
        """
        read boletín de asturias
        :param: the webdriver in use at the moment
        """
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                         "/html/body/div[2]/div[2]/div/div/div/div["
                                                                         "3]/div/div[3]/div/p[1]")))
        # lee objeto de regulación y texto
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div/div/div/div[3]/div/div[3]/div/p[1]").text
        Writer.datos_disposicion["texto_completo"] = self.sacar_texto_asturias_html(browser)
        Writer.datos_disposicion["boletin"] = "Boletín Oficial del Principado de Asturias"

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_asturias(browser):
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         ".pdfResultadoBopaLogo > a:nth-child("
                                                                         "1)"))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        self.process_disposition()

    @staticmethod
    def sacar_objeto_regulacion_canarias_html(browser):
        """
        extracts the heading of boe canarias
        :return: objeto de regulacion
        """
        pattern = re.compile(r"\d* página")
        s = browser.find_element_by_xpath("/html/body/div/div[4]/div[2]/div/h3").text[
            5:re.search(pattern, browser.find_element_by_xpath("/html/body/div/div[4]/div[2]/div/h3").text).start()]
        return s

    @staticmethod
    def pdf_canarias(browser):
        """
        in aragon there are no images, for what i know
        :param browser:
        :return:
        """
        try:
            browser.find_element_by_class_name("justificado anexo")
            return True
        except NoSuchElementException:
            pass

        try:
            browser.find_element_by_class_name("conten").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            pass
        try:
            browser.find_element_by_class_name("conten").find_element_by_tag_name("img")
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def sacar_texto_canarias_html(browser):
        """
        extract full text from boe canarias
        :param browser: current selenium driver
        :return: full text
        """
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

    def read_canarias_html(self, browser):
        """
        extracts data from boe canarias
        :param browser:
        """
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                         "/html/body/div/div[4]/div[2]/div/h3")))
        Writer.datos_disposicion["objeto_de_regulacion"] = self.sacar_objeto_regulacion_canarias_html(browser)
        Writer.datos_disposicion["texto_completo"] = self.sacar_texto_canarias_html(browser)
        Writer.datos_disposicion["boletin"] = "Boletín Oficial de Canarias"

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_canarias(browser):
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         ".cve > a:nth-child(2)"))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        self.process_disposition()

    @staticmethod
    def sacar_texto_leon_html(browser):
        s = ""
        try:

            i = 2  # i starts at 2 because the first <p> is the "objeto de regulación"
            t = True
            while t:
                s += browser.find_element_by_xpath(
                    "/html/body/div/div[2]/div/div/div[3]/div/div/p[" + str(i) + "]").text + "\n"
                i += 1
        except NoSuchElementException:
            pass
        return s

    @staticmethod
    def pdf_leon(browser):
        """
        in aragon there are no images, for what i know
        :param browser:
        :return:
        """
        try:
            browser.find_element_by_class_name("errorGenerico")
            return True
        except NoSuchElementException:
            pass

        try:
            browser.find_element_by_class_name("disposicion").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            pass
        try:
            browser.find_element_by_class_name("disposicion").find_element_by_tag_name("img")
            return True
        except NoSuchElementException:
            return False

    def read_leon_html(self, browser):
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                         "entradilla")))
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_class_name("entradilla").text
        Writer.datos_disposicion["texto_completo"] = self.sacar_texto_leon_html(browser)
        Writer.datos_disposicion["boletin"] = "Boletín Oficial de Castilla y León"

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_leon(browser):
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         ".descargaBoletin > li:nth-child(1) > "
                                                                         "a:nth-child(1)"))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        self.process_disposition()

    @staticmethod
    def pdf_catalunya(browser):
        """
        same as other pdf functions
        :param browser:
        :return:
        """

        try:
            browser.find_element_by_class_name("fitxaFragment").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            pass
        try:
            browser.find_element_by_class_name("fitxaFragment").find_element_by_tag_name("img")
            return True
        except NoSuchElementException:
            return False

    def read_catalunya_html(self, browser):
        WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "fitxaFragment")))
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_class_name("titol").text
        Writer.datos_disposicion["texto_completo"] = browser.find_element_by_class_name("fitxaFragment").text
        Writer.datos_disposicion["boletin"] = "Diari Oficial de la Generalitat de Catalunya"

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_catalunya(browser):
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         ".fitxaFormatsAkomantoso > div:nth-child(2) "
                                                                         "> ul:nth-child(1) > li:nth-child(1) > "
                                                                         "a:nth-child(1)"))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        self.process_disposition()

    @staticmethod
    def pdf_galicia(browser):
        """
        same as other pdf functions
        :param browser:
        :return:
        """

        try:
            browser.find_element_by_class_name("story").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            pass
        try:
            browser.find_element_by_class_name("story").find_element_by_tag_name("img")
            return True
        except NoSuchElementException:
            return False

    def read_galicia_html(self, browser):
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                         "dog-texto-sumario")))
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_class_name("dog-texto-sumario").text
        Writer.datos_disposicion["texto_completo"] = browser.find_element_by_class_name("story").text
        Writer.datos_disposicion["boletin"] = "Diario Oficial de Galicia"

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_galicia(browser):
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         ".documentoPDF"))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        self.process_disposition()

    @staticmethod
    def pdf_larioja(browser):
        """
        same as other pdf functions
        :param browser:
        :return:
        """

        try:
            browser.find_element_by_class_name("anuncio_texto").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            pass
        try:
            browser.find_element_by_class_name("anuncio_texto").find_element_by_tag_name("img")
            return True
        except NoSuchElementException:
            return False

    def read_larioja_html(self, browser):
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                         "entradilla_anuncio")))
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_class_name("entradilla_anuncio").text
        Writer.datos_disposicion["texto_completo"] = browser.find_element_by_class_name("anuncio_texto").text
        Writer.datos_disposicion["boletin"] = "Boletín Oficial de La Rioja"

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_larioja(browser):
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         "div.page-header:nth-child(2) > "
                                                                         "div:nth-child(2) > a:nth-child(1)"))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        self.process_disposition()

    @staticmethod
    def pdf_madrid(browser):
        """
        same as other pdf functions
        :param browser:
        :return:
        """

        try:
            browser.find_element_by_id("cuerpo").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            pass
        try:
            browser.find_element_by_id("cuerpo").find_element_by_tag_name("img")
            return True
        except NoSuchElementException:
            return False

    def read_madrid_html(self, browser):
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID,
                                                                         "cuerpo")))
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_id("entradilla").text
        Writer.datos_disposicion["texto_completo"] = browser.find_element_by_id("cuerpo").text
        Writer.datos_disposicion["boletin"] = "Boletín Oficial de la Comunidad de Madrid"

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_madrid(browser):
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         "#titulo_cabecera > h2:nth-child(5) > "
                                                                         "a:nth-child(1)"))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        self.process_disposition()

    @staticmethod
    def pdf_murcia(browser):
        """
        same as other pdf functions
        :param browser:
        :return:
        """

        try:
            browser.find_element_by_class_name("contenidoAnuncio").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            pass
        try:
            browser.find_element_by_class_name("contenidoAnuncio").find_element_by_tag_name("img")
            return True
        except NoSuchElementException:
            return False

    def read_murcia_html(self, browser):
        WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div[3]/div[2]/div/div/h1")))
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_class_name("ng-binding").text
        Writer.datos_disposicion["texto_completo"] = browser.find_element_by_id("contenidoAnuncio").text
        Writer.datos_disposicion["boletin"] = "Boletín Oficial de la Región de Murcia"

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_murcia(browser):
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         ".btn-doc-pdf"))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        self.process_disposition()

    @staticmethod
    def sacar_texto_navarra_html(browser):
        s = ""
        try:

            i = 2  # i starts at 2 because the first <p> is something else
            t = True
            while t:
                s += browser.find_element_by_xpath(
                    "/html/body/div/main/section/div/div[2]/div[1]/div/div/section/div/div/div/p[" + str(
                        i) + "]").text + "\n"
                i += 1
        except NoSuchElementException:
            pass
        return s

    @staticmethod
    def pdf_navarra(browser):
        """
        same as other pdf functions
        :param browser:
        :return:
        """

        try:
            browser.find_element_by_class_name("portlet-body").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            pass
        try:
            browser.find_element_by_class_name("portlet-body").find_element_by_tag_name("img")
            return True
        except NoSuchElementException:
            return False

    def read_navarra_html(self, browser):
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                         "/html/body/div/main/section/div/div[2]/div["
                                                                         "1]/div/div/section/div/div/div/h3[2]")))
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_xpath(
            "/html/body/div/main/section/div/div[2]/div[1]/div/div/section/div/div/div/h3[2]").text
        Writer.datos_disposicion["texto_completo"] = self.sacar_texto_navarra_html(browser)
        Writer.datos_disposicion["boletin"] = "Boletín Oficial de Navarra"

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_navarra(browser):
            Writer.datos_disposicion["pdf"] = True
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        self.process_disposition()

    @staticmethod
    def sacar_texto_vasco_html(browser):
        s = ""
        try:

            i = 3  # i starts at 2 because the first <p> is something else
            t = True
            while t:
                s += browser.find_element_by_xpath(
                    "/html/body/div[1]/div[4]/div/div/div/div[2]/div/p[" + str(i) + "]").text + "\n"
                i += 1
        except NoSuchElementException:
            pass
        return s

    @staticmethod
    def pdf_vasco():
        """
        same as other pdf functions
        :return:
        """
        if "(Véase el .PDF)" in Writer.datos_disposicion["texto_completo"]:
            return True

    def read_vasco_html(self, browser):
        WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/div[4]/div/div/div/div[2]/div/p[2]")))
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_class_name("BOPVTitulo").text
        Writer.datos_disposicion["texto_completo"] = self.sacar_texto_vasco_html(browser)
        Writer.datos_disposicion["boletin"] = "Boletín Oficial del País Vasco"

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_vasco():
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         ".formatoPdf > a:nth-child(1)"))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        self.process_disposition()

    @staticmethod
    def pdf_valencia(browser):
        """
        same as other pdf functions
        :param browser:
        :return:
        """

        try:
            browser.find_element_by_class_name("fic2").find_element_by_tag_name("table")
            return True
        except NoSuchElementException:
            pass
        try:
            browser.find_element_by_class_name("fic2").find_element_by_tag_name("img")
            return True
        except NoSuchElementException:
            return False

    def read_valencia(self, browser):
        WebDriverWait(browser, 20).until(EC.frame_to_be_available_and_switch_to_it("iframe-164029406"))
        WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "negro")))
        Writer.datos_disposicion["objeto_de_regulacion"] = browser.find_element_by_class_name("negro").text
        Writer.datos_disposicion["texto_completo"] = browser.find_element_by_id("fic2").text
        Writer.datos_disposicion["boletin"] = "Diari Oficial de la Comunitat Valenciana"

        if len(Writer.datos_disposicion["texto_completo"]) > 60000 or self.pdf_valencia(browser):
            Writer.datos_disposicion["pdf"] = True
            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         ".btnPDF"))).click()
            Writer.datos_disposicion["texto_completo"] = Writer.datos_disposicion["texto_completo"][:60000]

        self.process_disposition()

    def read_disposicion_html(self, url, browser):
        """
        Case Boletín Oficial del Estado
        """
        if "boe.es" in url:
            self.read_boe_html(browser)
        elif "juntadeandalucia" in url:
            self.read_boja_html(browser)
        elif "boa.aragon" in url:
            self.read_aragon_html(browser)
        elif "sede.asturias" in url:
            self.read_asturias_html(browser)
        elif "gobiernodecanarias" in url:
            self.read_canarias_html(browser)
        elif "bocyl" in url:
            self.read_leon_html(browser)
        elif "dogc.gencat" in url:
            self.read_catalunya_html(browser)
        elif "xunta.gal" in url:
            self.read_galicia_html(browser)
        elif "web.larioja" in url:
            self.read_larioja_html(browser)
        elif "borm" in url:
            self.read_murcia_html(browser)
        elif "bon.navarra" in url:
            self.read_navarra_html(browser)
        elif "euskadi" in url:
            self.read_vasco_html(browser)
        elif "dogv.gva" in url:
            self.read_valencia(browser)
        elif "bocm" in url:
            self.read_madrid_html(browser)


""" puedo asignar a los método del otro módulo el nombre de una variable para poder usarlo sin que esté tan petado de 
cosas"""
