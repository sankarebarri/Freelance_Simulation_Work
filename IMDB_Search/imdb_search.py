from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import Select
import pandas as pd

s = Service(r'C:\Users\sanka\Desktop\data\chromdriver\chromedriver.exe')
driver = webdriver.Chrome(service=s)

driver.get('https://www.imdb.com/')
driver.maximize_window()
time.sleep(5)

#the  dropdown in the homepage search
dropdown = driver.find_element(By.ID, "iconContext-arrow-drop-down")
dropdown.click()

#advance search link
advance_search = driver.find_element(By.LINK_TEXT, 'Advanced Search')
advance_search.click()

advance_title_search = driver.find_element(By.LINK_TEXT, 'Advanced Title Search')
advance_title_search.click()
time.sleep(5)

#select the radio buttons for title type
documentary = driver.find_element(By.ID, 'title_type-7')
documentary.click()

tv_series = driver.find_element(By.ID, 'title_type-9')
tv_series.click()

short_film = driver.find_element(By.ID, 'title_type-3')
short_film.click()

#type in release date year
release_date_min = driver.find_element(By.NAME, "release_date-min") 
release_date_min.click()
release_date_min.send_keys('2010')

release_date_max = driver.find_element(By.NAME, "release_date-max") 
release_date_max.click()
release_date_max.send_keys('2020')

#select the users rating
user_rating_min = driver.find_element(By.NAME, 'user_rating-min')
user_rating_min.click()
dropdown_2 = Select(user_rating_min)
dropdown_2.select_by_visible_text('1.0')

user_rating_max = driver.find_element(By.NAME, 'user_rating-max')
user_rating_max.click()
dropdown_2 = Select(user_rating_max)
dropdown_2.select_by_visible_text('10')

#select genre type
action = driver.find_element(By.ID, 'genres-1')
action.click()

#select title data
title_data_plot = driver.find_element(By.XPATH, "(//select[@name='has']/option)[7]")
title_data_plot.click()

title_data_xray = driver.find_element(By.XPATH, "(//select[@name='has']/option)[12]")
title_data_xray.click()

#select film languages
languages = driver.find_element(By.XPATH, "(//select[@name='languages']/option)[80]")
languages.click()

#select display options for film per page
display_option = driver.find_element(By.ID, 'search-count')
display_option.click()
dropdown_3 = Select(display_option)
dropdown_3.select_by_index(2)

#click on the search button 
search = driver.find_element(By.XPATH, "(//button[@type='submit'])[2]")
search.click()

###### BEAUTIFUL SOUP TO SCRAPE THE TITLE, YEAR, DURATION, GENRE, RATING ######
from bs4 import BeautifulSoup as bs
import requests

response = requests.get(current_url)
response.status_code

soup = bs(response.content, 'html.parser')

list_items = soup.find_all('div', {'class':'lister-item'})
len(list_items)

title = list_items[0].find('h3').find('a').get_text()
print(title)

year = list_items[0].find('h3').find('span', {'class': 'lister-item-year'}).get_text().replace("(", "").replace(")","")
print(year)

duration = list_items[0].find('span',{'class': 'runtime'}).get_text()
print(duration)

genre = list_items[0].find('span', {'class': 'genre'}).get_text().strip()

#list_items[0].find('div', {'class': 'ratings-bar'}).get_text().strip()
rating = list_items[0].find('strong').get_text()
print(rating)

imdb_data = []
for item in list_items:
    temporary_data = {
        'Title': item.find('h3').find('a').get_text(),
        'Year': item.find('h3').find('span', {'class': 'lister-item-year'}).get_text().replace("(", "").replace(")",""),
        'Time': item.find('span',{'class': 'runtime'}).get_text(),
        'Genre': item.find('span', {'class': 'genre'}).get_text().strip(),
        'Rating': item.find('strong').get_text(),
    }
    
    imdb_data.append(temporary_data)
    


imdb_data = pd.DataFrame(imdb_data)
imdb_data
imdb_data.to_excel('imdb_data.xlsx',index=False)
