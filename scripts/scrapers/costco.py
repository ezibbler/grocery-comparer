import requests
from bs4 import BeautifulSoup
import re

def __main__():
    #gets all products in the costco database
    #TODO: get prices from costco site and add them into csv
    products = recursive_get("https://costcofdb.com/food-database", "https://costcofdb.com/product-category")

def find_links(origin : str, target : str, final : bool = False):
    #gets target links from base link

    r = requests.get(origin)
    regexed_target = target.replace("/", "\/").replace(".", "\.")

    soup = BeautifulSoup(r.content, "html.parser")
    soup = soup.prettify()

    #finds links to categories
    if final:
        #gets list of products
        links = re.findall(f"href=\"(https:\/\/costcofdb\.com\/product\/[^\/\"]+?)\"", soup)
    else:
        links = re.findall(f"aria-label=\"[^\/\"]+?\" href=\"({regexed_target}\/[^\/\"]+?)\"", soup)

    #find unique values
    values = []
    for link in links:
        if link in values:
            continue
        else:
            values.append(link)
    return values

def recursive_get(origin : str, target : str):
    #get each link on page
    links = find_links(origin, target)

    #if there are no subcategory links
    if links == []:
        #get the product links
        return find_links(origin, origin, final=True)
    else:
        #get the links contained in all subpages and add them to a list
        products = []
        for link in links:
            print(link)
            products.extend(recursive_get(link, link))
        return products

if __name__ == "__main__":
    __main__()