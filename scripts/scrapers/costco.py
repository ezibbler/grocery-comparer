import requests
from bs4 import BeautifulSoup
import re

def __main__():
    #gets html of main costco page
    r = requests.get("https://costcofdb.com/food-database")

    soup = BeautifulSoup(r.content, "html.parser")
    soup = soup.prettify()

    #finds links to categories
    links = re.findall("href=\"(https:\/\/costcofdb\.com\/product-category\/[^\/\"]+?)\"", soup)

    #find unique values
    values = []
    for link in links:
        if link in values:
            continue
        else:
            values.append(link)

    print(join(values, joiner="\n"))

def join(list, joiner = ""):
    joined = ""
    for element in list:
        joined += str(element) + joiner
    return joined

def nice_print(list):
    result = ""

if __name__ == "__main__":
    __main__()