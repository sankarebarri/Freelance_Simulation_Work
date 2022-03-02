from requests_html import HTMLSession
import csv

s = HTMLSession()

def agent_link(page):
    links = []
    url = f'https://www.yellowpages.net/places/property-sales/{page}.html'

    r = s.get(url)

    agency = r.html.find('div.cc-content')
    #print(agency.find('a'))

    for agent in agency:
        #print(agent.text)
        links.append(agent.find('a', first=True).attrs['href'])

    return links

def get_agent_details(url):
    #url = 'https://www.yellowpages.net/profil,116692,vihav-realty-pvt-ltd,vadodara.html'

    r = s.get(url)
    try:
        name = r.html.find('h1', first=True).text
    except:
        name = 'No name'
    try:
        address = r.html.find('address', first=True).text.replace('place\n', '')
    except:
        address = 'No address'
    try:
        phone = r.html.find('div.cc_phones_list', first=True).text
    except:
        phone = 'Not provided'
    try:
        website = r.html.find('div.urls', first=True).text
    except:
        website = 'No website provided'
    try:
        description = r.html.find('div.card-description', first=True).text
    except:
        description = 'No description'
    #print(name, address, phone, website, description)
    details = {
        'name': name,
        'address': address,
        'phone': phone,
        'website': website,
        'description': description,
    }
    return details

def save_as_csv(results):
    keys = results[0].keys()

    with open('agents.csv', 'w', encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

#for link in agent_link('https://www.yellowpages.net/places/property-sales/1.html'):
    #print(get_agent_details(link))
    #print('\n')

def main():
    results = []
    for i in range(1, 10):
        print('scraping page', i)
        links = agent_link(i)
        for link in links:
            results.append(get_agent_details(link))
            #print('\n')
        save_as_csv(results)

if __name__ == '__main__':
    main()
