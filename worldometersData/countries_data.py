from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.service import Service

s = Service(r'C:\Users\sanka\Desktop\data\chromdriver\chromedriver.exe')
driver = webdriver.Chrome(service=s)

driver.get('https://www.worldometers.info/world-population/population-by-country/')
driver.maximize_window()


countries = driver.find_elements(By.XPATH, "//table[@id='example2']/tbody/tr/td[2]/a")
populations = driver.find_elements(By.XPATH, "//table[@id='example2']/tbody/tr/td[3]")
land_area = driver.find_elements(By.XPATH, "//table[@id='example2']/tbody/tr/td[7]")
fert_rate = driver.find_elements(By.XPATH, "//table[@id='example2']/tbody/tr/td[9]")
urban_prop = driver.find_elements(By.XPATH, "//table[@id='example2']/tbody/tr/td[11]")
world_share = driver.find_elements(By.XPATH, "//table[@id='example2']/tbody/tr/td[12]")

# Create a dictionary for each item
countries_data = []
for i in range(len(countries)):
    temporary_data = {
        'Countries': countries[i].text,
        'Populations': populations[i].text,
        'Land_area': land_area[i].text,
        'Fert_rate': fert_rate[i].text,
        'Urban_prop': urban_prop[i].text,
        'World_share': world_share[i].text,
    }
    countries_data.append(temporary_data)

#convert to pandas dataframe
df = pd.DataFrame(countries_data)

#convert to different formats
df.to_csv('population.csv')
df.to_excel('population.xlsx', index=False)
df.to_json('population.json')
