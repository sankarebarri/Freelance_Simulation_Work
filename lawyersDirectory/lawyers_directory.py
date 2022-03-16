from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

s = Service(r'C:\Users\sanka\Desktop\data\chromdriver\chromedriver.exe')
driver = webdriver.Chrome(service=s)

total_data = []
for page in range(1, 90):
    url = f'https://www.floridabar.org/directories/find-mbr/?lName=&sdx=N&fName=&eligible=N&deceased=N&firm=&locValue=&locType=C&pracAreas=P02&lawSchool=&services=&langs=&certValue=&pageNumber={page}&pageSize=50'
    driver.get(url)
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    
    names = soup.find_all('p', {'class':'profile-name'})
    real_names = []
    
    for name in names:
        if name.get_text().startswith('"') == False:
            real_names.append(name.get_text())
    
    bar_number = soup.find_all('p', {'class':'profile-bar-number'})
    
    companies = driver.find_elements_by_class_name('profile-contact')
    sel_companies = []
    for company in companies:
        sel_companies.append(company.text)
        
    main_data1 = []
    for i in range(50):
        try:
            email_address = sel_companies[i].split('\n')[-1]
        except:
            email_address = 'Not provided'
        try:
            company = sel_companies[i].split('\n')[0]
        except:
            company = 'Not provided'
        try:
            address = sel_companies[i].split('\n')[1]
        except:
            address = 'Not provided'
        try:
            city = sel_companies[i].split('\n')[2].split(',')[0]
        except:
            city = 'Not provided'
        try:
            state = sel_companies[i].split('\n')[2].split(',')[1].strip().split(' ')[0]
        except:
            state = 'Not provided'
        try:
            state_zip = sel_companies[i].split('\n')[2].split(',')[1].strip().split(' ')[1]
        except:
            state_zip = 'Not provided'
        try:
            phone = sel_companies[i].split('\n')[3].split(':')[1].strip()
        except:
            phone = 'Not provided'
        try:
            website = sel_companies[i].split('\n')[-1].split('@')[1]
        except:
            website = 'Not provided'
        try:
            first = real_names[i].split(' ')[0]
        except:
            first = 'Not provided'
        try:
            last = real_names[i].split(' ')[-1]
        except:
            last = 'Not provided'
        try:
            bar = bar_number[i].get_text().replace('Bar #','')
        except:
            bar = 'Not provided'
        temporary_data = {
            'Email Address': email_address,
            'Company': company,
            'Address': address,
            'City': city,
            'State': state,
            'Zip': state_zip,
            'Phone': phone,
            'Website': website,
            'lo1': 'PI',
            'lo2-bar #': bar,
            'part': '',
            'First': first,
            'Last': last,
        }
        main_data1.append(temporary_data)
        if page == 89:
            break
    total_data.extend(main_data1)

df = pd.DataFrame(total_data)

#formats
df.to_excel('personal_injury.xlsx', index=False)
df.to_csv('personal_injury.csv')
df.to_json('personal_injury.json')