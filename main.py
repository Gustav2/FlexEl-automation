from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

url = "https://norlys.dk/kundeservice/el/flexel-prisudvikling"

options = Options()
options.add_argument("--headless")
drive = webdriver.Firefox(options=options)

drive.get(url)

content = BeautifulSoup(drive.page_source, "html.parser")


def find_cheapest_time():
    root = content.find("div", {"id": "root"})
    # cheapest = root.find(lambda tag:tag.name=="p" and "time" in tag.text)
    cheapest = root.find("div", {"data-testid": "flex-el_cheapest-price-indicator"})

    for child in cheapest.children:
        if "Kl" in child.getText():
            unparsed = child.getText().replace(".", "").split(" ")
            timeinterval = []
            for i in unparsed:
                if i.isnumeric():
                    timeinterval.append(i)

            return timeinterval


print(find_cheapest_time())
