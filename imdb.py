# SPDX-License-Identifier: MIT
# (C) 2024 The Elvis Kipkosgei Mwogoi
# (C)  Israel Dryer tutorials

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.google.com/')


box = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea')
#print(driver.page_source)
box.send_keys('top 100 movies of all time imdb')
box.send_keys(Keys.ENTER)
time.sleep(10)
driver.find_element(By.XPATH,'/html/body/div[3]/div/div[13]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/div/div/span/a/h3').click()
time.sleep(20)
# Scroll down to bottom
driver.execute_script("window.scrollTo(0,8888);")
time.sleep(10)
driver.find_element(By.XPATH,'/html/body/div[2]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span').click()
time.sleep(10)
#driver.execute_script('window.scrollTo(0, 12000)')
#time.sleep(10)

#driver.save_screenshot('elvo_imdb_screenshot.png')
# Creates a dataframe
df = pd.DataFrame({'Link': [''], 'title': [''], 'description': [''], 'Years': [''], 'Hours': [''], 'Rated': ['']})
#'Rated': ['']
# This loop goes through every page and grabs all the details of each posting
# Loop will only end when there are no more pages to go through

# Imports the HTML of the current page into python
soup = BeautifulSoup(driver.page_source, 'lxml')

# Grabs the HTML of each posting
movies = soup.find_all('li', class_='ipc-metadata-list-summary-item')

# grabs all the details for each posting and adds it as a row to the dataframe
for movie in movies:
    link = movie.find('a', class_='ipc-title-link-wrapper').get('href')
    link_full = 'https://www.imdb.com/' + link
    Title = movie.find('h3', class_='ipc-title__text').text.strip()
    Description = movie.find('div', class_='ipc-html-content-inner-div').text.strip()
    tag = movie.select('.sc-b189961a-8')
    try:
        Years = tag[0].get_text()
        Hours = tag[1].get_text()
        Rated = tag[2].get_text()
    except IndexError:
        Rated = None
    df = df._append(
            {'Link': link_full, 'Title': Title,'Description': Description ,'Years': Years, 'Hours': Hours, 'Rated': Rated
             },
            ignore_index=True)
            
  

df = df[['Link', 'Title', 'Description', 'Years', 'Hours', 'Rated']]

df.to_csv('imdb_scraped_data.csv')


