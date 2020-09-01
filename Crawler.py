from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup

"""
This file contains the functions that look for the documents that interest us


Antes de ejecutar cada uno de los boletines autonómicos hay que 
ir a "https://boe.es/legislacion/otros_diarios_oficiales.php#boletines_autonomicos" , 
y de ahi clickar en el correspondiente, que estará almacenado en un dict
"""

# these are the words we are looking for in the text of the dispositions
palabras_buscar_disposiciones = ["universidad", "formación profesional", "educación", "educativo", "docente", "idiomas",
                                 "enseñanza", "concierto educativo", "conciertos educativos", "educación infantil",
                                 "educación secundaria", "bachillerato", "erasmus", "profesor", "catedrático", "alumn"]


def get_links_comunidades(browser):
    """
    saca el link de cada comunidad para asegurarnos de llegar siempre a la página adecuada
    """

    links_comunidades = {}

    browser.get("https://boe.es/legislacion/otros_diarios_oficiales.php#boletines_autonomicos")

    links_comunidades["andalucia"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[1]/li[1]/a")
    links_comunidades["aragon"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[2]/li/a")
    links_comunidades["asturias"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[3]/li/a")
    links_comunidades["canarias"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[5]/li[1]/a")
    links_comunidades["leon"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[8]/li[1]/a")
    links_comunidades["catalunya"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[9]/li[1]/a")
    links_comunidades["galicia"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[11]/li[1]/a")
    links_comunidades["rioja"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[12]/li[1]/a")
    links_comunidades["madrid"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[13]/li[1]/a")
    links_comunidades["murcia"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[14]/li[1]/a")
    links_comunidades["navarra"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[15]/li[1]/a")
    links_comunidades["vasco"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[16]/li[1]/a")
    links_comunidades["valencia"] = browser.find_element_by_xpath("/html/body/div[4]/div/div/ul/li[2]/ul[17]/li/a")

    return links_comunidades


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
            for palabra in palabras_buscar_disposiciones:
                if palabra in dispo_low \
                        and "extravío" not in dispo_low \
                        and "anuncio de formalización" not in dispo_low \
                        and "personal de administración y servicios" not in dispo_low \
                        and "libre designación" not in dispo_low \
                        and "asesor" not in dispo_low \
                        and "técnic" not in dispo_low:
                    link = dispo.find_element_by_class_name("puntoHTML").find_element_by_link_text(
                        "Otros formatos").get_attribute("href") + "\n"
                    urls.write(link)
                    break


def crawl_boja(browser, boja_link):
    """
    :param: boja_link es el elemento del dict links_comunidades que corresponde a andalucía
    """
    # opens the main webpage and gets into the first section
    boja_link.click()
    browser.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[1]/ol/li[1]/a").click()

    # scrapes each section for each iteration
    for i in range(2, 5):
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
                            for palabra in palabras_buscar_disposiciones:
                                if palabra in dispo_low \
                                        and "extravío" not in dispo_low \
                                        and "anuncio de formalización" not in dispo_low \
                                        and "personal de administración y servicios" not in dispo_low \
                                        and "libre designación" not in dispo_low \
                                        and "asesor" not in dispo_low \
                                        and "técnic" not in dispo_low:
                                    link = dispo.find_element_by_class_name("item_html").get_attribute("href") + "\n"
                                    urls.write(link)
                                    break
            except NoSuchElementException:
                continue

        # clicks on the next section to explore
        browser.find_element_by_xpath("/html/body/div[4]/div/div[2]/ol/li[" + str(i) + "]/a").click()


def crawl_aragon(browser, boa_link):
    """
    :param: boja_link es el elemento del dict links_comunidades que corresponde a aragon
    """
    # opens the mainpage and enters into the disposition list
    boa_link.click()

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
            for palabra in palabras_buscar_disposiciones:
                if palabra in text \
                        and "extravío" not in text \
                        and "anuncio de formalización" not in text \
                        and "personal de administración y servicios" not in text \
                        and "libre designación" not in text \
                        and "asesor" not in text \
                        and "técnic" not in text:
                    urls.write(link + "\n")
