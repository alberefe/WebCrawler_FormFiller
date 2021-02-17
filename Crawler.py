import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from datetime import date
import re
import time

"""
This file contains the functions that look for the documents that interest us


Antes de ejecutar cada uno de los boletines autonómicos hay que 
ir a "https://boe.es/legislacion/otros_diarios_oficiales.php#boletines_autonomicos" , 
y de ahi clickar en el correspondiente, que estará almacenado en un dict
"""

# these are the words we are looking for in the text of the dispositions
palabras_buscar_disposiciones = ["universid", "formación profesional", "educación", "educativo", "docente", "idiomas",
                                 "enseñanza", "concierto educativo", "conciertos educativos", "educación infantil",
                                 "educación secundaria", "bachillerato", "erasmus", "profesor", "catedrático", "alumn",
                                 "catedrátic"]


def select_crawler(browser, url):
    if "boe.es" in url:
        crawl_boe(browser)
    elif "juntadeandalucia" in url:
        crawl_boja(browser)
    elif "boa.aragon" in url:
        crawl_aragon(browser)
    elif "sede.asturias" in url:
        crawl_asturias(browser)
    elif "gobiernodecanarias" in url:
        crawler_canarias(browser)
    elif "bocyl" in url:
        crawler_leon(browser)
    elif "dogc.gencat" in url:
        crawler_catalunya(browser)
    elif "xunta.gal" in url:
        crawler_galicia(browser)
    elif "web.larioja" in url:
        crawler_rioja(browser)
    elif "borm" in url:
        crawler_murcia(browser)
    elif "bocm" in url:
        crawler_madrid(browser)
    elif "bon.navarra" in url:
        crawler_navarra(browser)
    elif "euskadi" in url:
        crawler_euskadi(browser)
    elif "dogv.gva" in url:
        crawler_valencia(browser)


def crawling_in_my_skin(browser):
    """
    Esta es la función principal del crawler que va a ir abriéndolo tod o y
    ejecutando el crawler de cada una
    """

    # el boe normal se ejecuta él solo
    crawl_boe(browser)

    # se abre la lista de comunidades, y luego se sacan los links y se van clickando
    browser.get("https://boe.es/legislacion/otros_diarios_oficiales.php#boletines_autonomicos")
    links = get_links_comunidades(browser)
    for link in links:
        browser.get(link)
        # browser.switch_to.window(browser.window_handles[1])
        select_crawler(browser, link)


def get_links_comunidades(browser):
    """
    saca el link de cada comunidad para asegurarnos de llegar siempre a la página adecuada
    """

    urls_comunidades = [
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[1]/li[1]/a").get_attribute("href"),
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[2]/li/a").get_attribute("href"),
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[3]/li/a").get_attribute("href"),
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[5]/li[1]/a").get_attribute("href"),
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[8]/li[1]/a").get_attribute("href"),
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[9]/li[1]/a").get_attribute("href"),
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[11]/li[1]/a").get_attribute("href"),
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[12]/li[1]/a").get_attribute("href"),
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[13]/li[1]/a").get_attribute("href"),
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[14]/li[1]/a").get_attribute("href"),
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[15]/li[1]/a").get_attribute("href"),
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[16]/li[1]/a").get_attribute("href"),
        browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[17]/li/a").get_attribute("href")]

    return urls_comunidades


def check_disposicion(palabras, texto):
    for palabra in palabras:
        if palabra in texto \
                and "extravío" not in texto \
                and "anuncio de formalización" not in texto \
                and "personal de administración y servicios" not in texto \
                and "libre designación" not in texto \
                and "asesor" not in texto \
                and "técnic" not in texto \
                and "contencionso-administrativo" not in texto.lower():
            return True
    return False


def crawl_boe(browser):
    """
    Crawler que busca las disposiciones del BOE
    """
    browser.get("https://boe.es")
    browser.find_element_by_link_text("Último BOE").click()

    disposiciones = browser.find_elements_by_class_name("dispo")

    with open(r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt",
              "a") as urls:
        for dispo in disposiciones:
            dispo_low = dispo.text.lower()
            if check_disposicion(palabras_buscar_disposiciones, dispo_low):
                link = dispo.find_element_by_class_name("puntoHTML").find_element_by_link_text(
                    "Otros formatos").get_attribute("href") + "\n"
                urls.write(link)


def crawl_boja(browser):
    """

    """
    # opens the main webpage and gets into the first section
    browser.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[1]/ol/li[1]/a").click()

    # scrapes each section for each iteration
    for i in range(2, 6):
        # waits for the page to load
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div[2]/ul/li[1]/a")))

        # finds the list of dispositions
        items = browser.find_elements_by_class_name("item")

        for item in items:
            try:
                item.find_element_by_tag_name("h3")
                if "educación" in item.find_element_by_tag_name("h3").text.lower():
                    with open(
                            r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt"
                            , "a") as urls:
                        for dispo in item.find_elements_by_tag_name("div"):
                            dispo_low = dispo.find_element_by_tag_name("p").text.lower()
                            if check_disposicion(palabras_buscar_disposiciones, dispo_low):
                                link = dispo.find_element_by_class_name("item_html").get_attribute("href") + "\n"
                                urls.write(link)
            except NoSuchElementException:
                continue

        # clicks on the next section to explore
        try:
            next_section = browser.find_element_by_xpath("/html/body/div[4]/div/div[2]/ol/li[" + str(i) + "]/a")
            if "justicia" not in next_section.text:
                next_section.click()
        except NoSuchElementException:
            continue


def crawl_aragon(browser):
    """

    """

    # locates the frame by its number, 0, because it is the first frame on the page
    WebDriverWait(browser, 20).until(EC.frame_to_be_available_and_switch_to_it(0))

    # opens the dispositions list and changes tabs and closes the old one and stuff
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/a/span"))).click()

    """ esto de aquí da fallos a veces pero no recuerdo lo que hace. Habrá que revisarlo."""
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[1]/a[1]/img")))

    # from here, Beautiful Soup is used to parse the html and get the text
    url = browser.current_url
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    # abre el txt
    with open(
            r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt", "a") as urls:

        lista_disposiciones = soup.find_all("h5", {"class": "boatitulo"})

        for t in lista_disposiciones:
            text = t.text.lower().strip()
            part_link = t.find_next("a")["href"]
            link = 'http://www.boa.aragon.es' + part_link
            if check_disposicion(palabras_buscar_disposiciones, text):
                urls.write(link + "\n")


def crawl_asturias(browser):
    """

    """
    fecha_hoy = str(datetime.date.today().day) + "/" + str(datetime.date.today().month) + "/" + str(
        datetime.date.today().year)

    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                 '//*[@id="p_r_p_summaryDate"]'))).send_keys(fecha_hoy)

    browser.find_element_by_xpath(
        "/html/body/div[1]/div/section/div[4]/div/div/div/div[1]/section/div/div/div/div/div/div/div/div/div/div/div/div[1]/form/div[2]/button/span").click()

    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                 "/html/body/div[1]/div/section/div[4]/div/div/div/div/section/div/div[2]/div/div/div/div/div/fieldset/div/div/div/div/div[6]/div/div/div/a[2]")))

    soup = BeautifulSoup(requests.get(browser.current_url).content, 'html.parser')

    # finds all the disposiciones
    lista_disposiciones = soup.find_all("dt")

    with open(
            r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt", "a") as urls:
        for disposicion in lista_disposiciones:
            link = disposicion.find_next("a")["href"]
            if check_disposicion(palabras_buscar_disposiciones, disposicion.get_text()):
                urls.write(str(link) + "\n")


def crawler_canarias(browser):
    """
    pos eso
    """
    # entra en la página principal de las disposiciones
    browser.find_element_by_css_selector("p.justificado_boc:nth-child(2) > a:nth-child(1)").click()
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[4]/div[2]/div/div[1]/ul/li/a")))

    # crea el bs4 object
    url = browser.current_url
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    lista_disposiciones = soup.find_all("ul")

    with open(
            r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt", "a") as urls:
        for disposicion in lista_disposiciones:
            # aquí selecciona sólo los links que llevan al html
            links = disposicion.find_all("a", title="Vista previa (Versión no oficial)")
            text = disposicion.get_text()

            for link in links:
                link_url = "http://www.gobiernodecanarias.org" + link.get("href")
                if check_disposicion(palabras_buscar_disposiciones, text):
                    urls.write(str(link_url) + "\n")


def crawler_leon(browser):
    """
    crawler leon
    """
    # entra en la página principal de las disposiciones

    browser.find_element_by_css_selector(".acceso > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1)").click()
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div/div/div[3]/div[2]/p/a")))

    # crea el bs4 object
    url = browser.current_url
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    # primero recogemos todas las disposiciones en contenido, luego buscamos todos los párrafos
    contenido = soup.find("div", {"id": "resultados"})
    lista_disposiciones = contenido.find_all("p")

    with open(
            r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt", "a") as urls:
        for disposicion in lista_disposiciones:
            # aquí recoje tanto el link al pdf como al html
            links_raw = disposicion.find_next_sibling()
            links = links_raw.find_all("a")
            text = disposicion.get_text()
            for link in links:
                if "html/" in link["href"]:
                    link_url = "http://bocyl.jcyl.es/" + link["href"]
                    if check_disposicion(palabras_buscar_disposiciones, text):
                        urls.write(link_url + "\n")


def crawl_section_catalunya(browser):
    """
    función que busca en
    """
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div[1]/h1/a/img")))

    # crea el bs4 object
    url = browser.current_url
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    lista_disposiciones = soup.find_all("p", {"class": "separador negreta"})

    with open(
            r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt", "a") as urls:
        for disposicion in lista_disposiciones:
            # aquí selecciona sólo los links que llevan al html
            link = disposicion.find_next("a", title="Versión HTML")["href"]
            text = disposicion.get_text()
            if check_disposicion(palabras_buscar_disposiciones, text):
                urls.write(str(link) + "\n")


def crawler_catalunya(browser):
    """
    pues esto
    """
    # entra en la página principal de las disposiciones
    try:
        browser.find_element_by_css_selector(
            "#sumari > ul:nth-child(2) > li:nth-child(1) > form:nth-child(2) > a:nth-child(1)").click()

        crawl_section_catalunya(browser)

        try:
            browser.find_element_by_css_selector(
                "#sumari > ul:nth-child(2) > li:nth-child(2) > form:nth-child(2) > a:nth-child(1)").click()

            crawl_section_catalunya(browser)

        except NoSuchElementException:
            print("poner aquí un return porque ha acabado")

    except NoSuchElementException:
        try:
            browser.find_element_by_css_selector(
                "#sumari > ul:nth-child(2) > li:nth-child(2) > form:nth-child(2) > a:nth-child(1)").click()

            crawl_section_catalunya(browser)

        except NoSuchElementException:
            print("no hay disposiciones hoy, aquí hay que poner un return")


def crawler_galicia(browser):
    dia_hoy = str(date.today().day)
    browser.find_element_by_css_selector("[title*='Ver DOG del día " + dia_hoy).click()
    sections = ["I. Disposiciones generales", "II. Autoridades y personal", "III. Otras disposiciones",
                "IV. Oposiciones y concursos"]

    for section_name in sections:
        try:
            browser.find_element_by_link_text(section_name).click()

            # if there's no exception, it creates soup object and looks in it for the good stuff
            url = browser.current_url
            soup = BeautifulSoup(requests.get(url).content, 'html.parser')

            marco_disposiciones = soup.find("div", {"id": "fichaSeccion"})
            disposiciones = marco_disposiciones.findAll("li")

            with open(
                    r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt",
                    "a") as urls:

                # busca disposicion a disposicion
                for disposicion in disposiciones:
                    text = disposicion.get_text()
                    part_link = disposicion.find("a")["href"]
                    link = 'https://www.xunta.gal' + part_link
                    if check_disposicion(palabras_buscar_disposiciones, text):
                        urls.write(link + "\n")
        except NoSuchElementException:
            continue


def crawler_rioja(browser):
    disposiciones = browser.find_elements_by_css_selector("a[title='Texto Íntegro de la Disposición']")

    with open(
            r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt",
            "a") as urls:
        # busca disposicion a disposicion
        for disposicion in disposiciones:
            text = disposicion.text
            link = disposicion.get_attribute("href")

            if check_disposicion(palabras_buscar_disposiciones, text):
                urls.write(link + "\n")


def crawler_madrid(browser):
    browser.find_element_by_css_selector(
        ".field-name-field-content-name > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)").click()

    useful_sections = [section.get_attribute("href") for section in
                       browser.find_element_by_class_name("view-grouping-content").find_elements_by_tag_name("a") if
                       "UNIVERSIDAD" in section.text or "EDUCACIÓN" in section.text]

    for section in useful_sections:

        browser.get(section)

        soup = BeautifulSoup(requests.get(browser.current_url).content, 'html.parser')

        # finds all the disposiciones
        lista_disposiciones = soup.find_all("div", {
            "class": "field field-name-field-html-file field-type-file field-label-hidden"})

        with open(
                r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt",
                "a") as urls:

            for disposicion in lista_disposiciones:
                link = "http://www.bocm.es" + disposicion.find_next("a")["href"]
                text = disposicion.find_previous("div", {
                    "class": "field field-name-field-short-description field-type-text-long field-label-hidden"}).text

                if check_disposicion(palabras_buscar_disposiciones, text):
                    urls.write(link + "\n")


def crawler_murcia(browser):
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div/div[3]/div/div/div[3]/div/div/div/div/div/p[2]/a"))).click()


    time.sleep(10)
    html = browser.page_source

    soup = BeautifulSoup(html, 'html.parser')

    # finds all the disposiciones
    lista_disposiciones = soup.find_all("a", title="Ver anuncio")

    with open(
            r"C:\\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt",
            "a") as urls:
        for disposicion in lista_disposiciones:
            link = "http://www.bocm.es" + disposicion["href"]
            text = disposicion.find_previous_sibling().find_previous_sibling().find_previous_sibling().text

            if check_disposicion(palabras_buscar_disposiciones, text):
                urls.write(link + "\n")


def crawler_navarra(browser):
    """

    """
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/main/section/div/div[2]/div[1]/div/div[2]/section/div/div/div/p[1]/a")))

    soup = BeautifulSoup(requests.get(browser.current_url).content, 'html.parser')

    # finds all the disposiciones from an anchor link
    anchor_link = soup.find("p", {"class": "pdf-link hidden-print"})

    print(anchor_link.text)
    lista_disposiciones = anchor_link.find_next_siblings("p")

    for i in lista_disposiciones:
        print(i.text)

    with open(r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt",
              "a") as urls:
        for disposicion in lista_disposiciones:
            link = disposicion.find_next("a")["href"]
            text = disposicion.text
            if check_disposicion(palabras_buscar_disposiciones, text):
                urls.write(link + "\n")


def crawler_euskadi(browser):
    url = browser.current_url
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    pattern = re.compile(".+?(?=Ultimo)")
    part_link_1 = pattern.match(url).group(0)

    with open(
            r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt", "a") as urls:
        lista_disposiciones = soup.find_all("p", {"class": "BOPVSumarioTitulo"})

        for dispo in lista_disposiciones:
            text = dispo.text.lower().strip()
            part_link_2 = dispo.find("a")["href"]
            link = part_link_1 + part_link_2
            if check_disposicion(palabras_buscar_disposiciones, text):
                urls.write(link + "\n")


def crawler_valencia(browser):
    WebDriverWait(browser, 20).until(
        EC.frame_to_be_available_and_switch_to_it(browser.find_element_by_xpath("//*[@id='iframe-164029029']")))

    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div[2]/div[2]/ul/li[2]/a")))

    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    part_link_1 = "http://www.dogv.gva.es/es"
    disposiciones = soup.find_all("li", {"class": "enlaceHTML"})

    with open(
            r"C:\\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt",
            "a") as urls:
        for dispo in disposiciones:
            part_link_2 = dispo.find_next("a")["href"]

            text = dispo.find_previous("div", {"class": "Organismo"}).find_next(string=True).find_next(
                string=True).strip().lower()
            link = part_link_1 + part_link_2

            if check_disposicion(palabras_buscar_disposiciones, text):
                urls.write(link + "\n")
