import requests
from bs4 import BeautifulSoup
import re

def __main__():
    products = find_links("https://www.instacart.com/categories")

    #csv = open("products.csv", "w")
    for product in products:
        for item in product["items"]:
            print(item)
            #csv.write(f"{item["link"]}, {item["price"]}")
    print(*products)

def find_links(origin : str):
    values = []

    #gets target links from base link
    r = requests.get(origin)

    soup = BeautifulSoup(r.content, "html.parser")
    #soup = soup.prettify()

    #finds links to categories
    items = soup.find_all("a", class_="e-1r6gosf")

    for item in items:
        name = item.find("div", class_="e-gaeqab")

        #eliminates non-food categories
        if item["href"].find("316-food") == -1:
            print(item["href"])
            break

        if name:
            values.append({
                "link": item['href'],
                "name": name.get_text().strip(),
                "items" : get_product_links(f"https://www.instacart.com{item['href']}")
            })

    return values

def get_product_links(origin : str):
    values = []

    #gets target links from base link
    r = requests.get(origin)

    soup = BeautifulSoup(r.content, "html.parser")
    #soup = soup.prettify()

    #finds links to categories
    items = soup.find_all("a", class_="e-18zipbc")

    for item in items:
        count = item.find("div", class_="e-an4oxa")

        if count:
            values.append({
                "link": item['href'],
                "count": count.get_text().strip(),
                "price": find_price(f"https://www.instacart.com{item['href']}")
            })

    return values


def find_price(link : str):
    #gets target links from base link
    r = requests.get(link)

    soup = BeautifulSoup(r.content, "html.parser")

    #finds links to categories
    price = soup.find_all("div", class_="e-dzwvfb")

    if not price:
        return "no price"
    
    print(f"{link}\n{price.get_text().strip()}")

    return price.get_text().strip()

if __name__ == "__main__":
    __main__()