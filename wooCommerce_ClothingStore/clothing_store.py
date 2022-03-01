from requests_html import HTMLSession
import csv

s = HTMLSession()

#url_test = 'https://themes.woocommerce.com/storefront/product/lowepro-slingshot-edge-250-aw/'

#r = s.get(url_test)

#name = r.html.find('h1.product_title', first=True).text
#price = r.html.find('p.price', first=True).text.replace('£', '')
#sku = r.html.find('span.sku', first=True).text
#cat = r.html.find('span.posted_in a', first=True).text
#print(name, price, sku, cat)

#print(item_info('https://themes.woocommerce.com/storefront/product/blue-shoes/'))


#r.html.find('h1.product_title.entry-title', first=True)

def get_links_of_each_items(page):
    url = f'https://themes.woocommerce.com/storefront/product-category/clothing/page/{page}'
    r = s.get(url)
    links = []
    products = r.html.find('ul.products li')
    for item in products:
        links.append(item.find('a', first=True).attrs['href'])

    return links



def item_info(url_link):
    r = s.get(url_link)
    name = r.html.find('h1.product_title', first=True).text
    price = r.html.find('p.price', first=True).text.replace('£', '')
    try:
        sku = r.html.find('span.sku', first=True).text
    except:
        sku = 'Empty'
    cat = r.html.find('span.posted_in a', first=True).text
    product = {
        'name': name,
        'price': price,
        'sku': sku,
        'category': cat
    }
    return product
#print(get_links_of_each_items(1))

def save_to_csv(results):
    keys = results[0].keys()

    with open('product.csv', 'w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

results = []
for i in range(1, 5):
    pages = get_links_of_each_items(i)
    print('Scraping page' ,i)
    for link in pages:
        results.append(item_info(link))
    save_to_csv(results)

print('Finished')
print('Check Products.csv')
#print(results)
