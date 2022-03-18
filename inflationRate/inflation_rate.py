import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

#connecting to the website
s = Service(r'C:\Users\sanka\Desktop\data\chromdriver\chromedriver.exe')
driver = webdriver.Chrome(service=s)
url = 'https://www.theglobaleconomy.com/rankings/inflation_outlook_imf/'
driver.get(url)
driver.maximize_window()

year_list = [str(year) for year in range(2000, 2027)]

#scraping the pages
main_data = []
for i in range(len(year_list)):
    year = driver.find_element(By.ID, 'year')
    year.click()
    year_dropdown = Select(year)
    year_dropdown.select_by_visible_text(year_list[i])
    
    countries = driver.find_elements(By.CLASS_NAME, 'graph_outside_link')
    all_countries = []
    for country in countries:
        all_countries.append(country.text)
        
    rates = driver.find_elements(By.XPATH, '//*[@id="content"]/div[2]/div[3]/div[5]/div[2]/div/div')
    
    index_rates = []
    for rate in rates:
        if rate.text != '':
            index_rates.append(rate.text)
            if len(index_rates) == len(countries):
                break
                
    temporary_data = dict(zip(all_countries, index_rates))
    main_data.append(temporary_data)


#convert the main_data to a dataframe
df = pd.DataFrame(main_data)

#create the years dataframe
years = pd.DataFrame(year_list, columns=['Year'])

#merge the df and df1 dataframe
inflation_rates = pd.concat([years,df], axis=1)