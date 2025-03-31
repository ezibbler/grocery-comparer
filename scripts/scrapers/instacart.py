import requests
from bs4 import BeautifulSoup
import re

def __main__():
    #gets all products in the costco database
    #TODO: get prices from costco site and add them into csv
    products = find_links("https://www.instacart.com/categories", "https://www.instacart.com/categories")
    print(*products)

def find_links(origin : str, target : str, final : bool = False):
    values = []
    #gets target links from base link

    r = requests.get(origin)
    regexed_target = target.replace("/", "\/").replace(".", "\.")

    soup = BeautifulSoup(r.content, "html.parser")
    #soup = soup.prettify()

    #finds links to categories
    items = soup.find_all("a", class_="e-1r6gosf")

    for item in items:
        name = item.find("div", class_="e-gaeqab")

        if name:
            values.append({
                "link": item['href'],
                "name": name.get_text().strip()
            })

    #find unique values

    return values

def find_price(link : str):
    r = requests.get(link)
    
    soup = BeautifulSoup(r.content, "html.parser")
    soup = soup.prettify()

    # with open("site.txt", "w") as f:
    #     f.write(soup)
    article = re.findall("<meta property=\"og:type\" content=\"article\" \/>", soup)
    #print(article)

    if len(article) == 0:
        return "Food item was listed as an article"

    price = re.findall("<meta content=\"(\d+.\d+)\" property=\"product:price:amount\"\/>", soup)
    if len(price) == 0:
        return "Food item was listed as an article"

    print(price)
    return price[0]

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
    
def extract_product_data(url: str):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        # Extract product name
        name = soup.find("h1", class_="product-title")
        name = name.text.strip() if name else "Unknown Product"

        # Extract product price using multiple approaches
        price = None

        # Option 1: Common class names for prices
        price_tags = soup.select('.price, .woocommerce-Price-amount, .product-price')
        for tag in price_tags:
            if tag.text.strip().startswith('$'):
                price = tag.text.strip()
                break

        # Option 2: Regular Expression Search
        if not price:
            price_text = soup.find(string=re.compile(r'\$\d+(\.\d{2})?'))
            price = price_text.strip() if price_text else "Price Not Available"
            
        print(f"Scraped: {name} - {price}")
        return {"name": name, "price": price, "url": url}

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

if __name__ == "__main__":
    __main__()