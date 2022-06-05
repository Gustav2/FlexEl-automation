import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

url = "https://norlys.dk/kundeservice/el/flexel-prisudvikling"

options = Options()
options.add_argument("--headless")
drive = webdriver.Firefox(options=options)

drive.get(url)

time.sleep(3)

content = BeautifulSoup(drive.page_source, "html.parser")


def find_cheapest_time():
    root = content.find("div", {"id": "root"})
    # cheapest = root.find(lambda tag:tag.name=="p" and "time" in tag.text)
    cheapest = root.find("div", {"data-testid": "flex-el_cheapest-price-indicator"})

    for child in cheapest.children:
        if "Kl" in child.getText():
            return child.getText()


print(find_cheapest_time())
