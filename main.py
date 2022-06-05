import time as t
from datetime import datetime, time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

url = "https://norlys.dk/kundeservice/el/flexel-prisudvikling"

"""
Adds option to enable headless mode.
This uses firefox Geckodriver to load page. Requires geckodriver to be installed. (win64 binary is included)
Replace with other engine if needed.
"""
options = Options()
options.add_argument("--headless")
drive = webdriver.Firefox(options=options)

# Fetches page
drive.get(url)

# Sleep to make sure the page is loaded
t.sleep(2)

# Parses fetched page with BS4
content = BeautifulSoup(drive.page_source, "html.parser")


# Parses HTML, finds cheapest timeinterval and returns timeinterval in ISO format
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

            return [i[:2] + ":" + i[2:] for i in timeinterval]


def check_time_in_interval(ti):
    return time.fromisoformat(ti[0]) <= datetime.now().time() <= time.fromisoformat(ti[1])


print(find_cheapest_time())
print(check_time_in_interval(find_cheapest_time()))

test = ['00:38', '02:00']
print(check_time_in_interval(test))
