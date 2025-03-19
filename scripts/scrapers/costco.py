import requests
from bs4 import BeautifulSoup
import re

def __main__():
    #gets html of main costco page
    values = find_links("https://costcofdb.com/food-database", "https://costcofdb.com/product-category")

    print(join(values, joiner="\n"))

def join(list, joiner = ""):
    joined = ""
    for element in list:
        joined += str(element) + joiner
    return joined

def find_links(link : str, target : str):
    r = requests.get(link)
    regexed_target = target.replace("/", "\/").replace(".", "\.")

    soup = BeautifulSoup(r.content, "html.parser")
    soup = soup.prettify()

    #finds links to categories
    links = re.findall(f"href=\"({regexed_target}\/[^\/\"]+?)\"", soup)

    #find unique values
    values = []
    for link in links:
        if link in values:
            continue
        else:
            values.append(link)
    return values

if __name__ == "__main__":
    __main__()