from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from datetime import date

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
        pass
    elif "bocyl" in url:
        crawler_leon(browser)
        pass
    elif "dogc.gencat" in url:
        pass
    elif "xunta.gal" in url:
        pass
    elif "web.larioja" in url:
        pass
    elif "borm" in url:
        pass
    elif "bon.navarra" in url:
        pass
    elif "euskadi" in url:
        pass
    elif "dogv.gva" in url:
        pass
    elif "bocm" in url:
        pass


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
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/p/a"))).click()
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/section/div/div/div/a[1]/img")))

    # from here, Beautiful Soup is used to parse the html and get the text
    url = browser.current_url
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    # abre el txt
    with open(
            r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt"
            , "a") as urls:

        # itera sobre cada texto + link y escribe el link si corresponde
        for t in soup.select('.archivos'):
            text = t.find_previous(text=True).strip().lower()
            part_link = t.a['href']
            link = 'http://www.boa.aragon.es' + part_link
            if check_disposicion(palabras_buscar_disposiciones, text):
                urls.write(link + "\n")


def crawl_asturias(browser):
    """

    """

    # mete fecha de hoy y entra en la lista de disposiciones
    browser.find_element_by_id("fecha").send_keys(str(date.today().strftime('%d/%m/%Y')))
    browser.find_element_by_css_selector("#btn-busq-BOPA-fecha").click()
    # espera a que la página se haya cargado
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".botonBuscar > input:nth-child(1)")))

    # creates a beautiful soup
    soup = BeautifulSoup(requests.get(browser.current_url).content, 'html.parser')

    # finds all the disposiciones
    lista_disposiciones = soup.find_all("dt")

    with open(
            r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt"
            , "a") as urls:
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
            r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt"
            , "a") as urls:
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
            r"C:\Users\DickVater\PycharmProjects\AutoMagislex\magislex\urls&pdfs\urls_disposiciones.txt"
            , "a") as urls:
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