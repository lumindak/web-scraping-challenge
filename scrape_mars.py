#!/usr/bin/env python
# coding: utf-8

# In[225]:


from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import urllib.request 
import pandas as pd


# In[184]:

def scrape():
  executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
  #headless=True will prebvent the browswer from opening
  browser = Browser('chrome', **executable_path, headless=True)

  # URL of page to be scraped
  url = 'https://mars.nasa.gov/news/'
  browser.visit(url)
  # Retrieve page with the requests module
  ##response = requests.get(url)
  # Create BeautifulSoup object; parse with 'lxml'
  #soup = BeautifulSoup(response.text, 'html.parser')


  # In[185]:


  html = browser.html
  soup = BeautifulSoup(html, 'html.parser')

  news= soup.find_all('div',class_='content_title')


  #print('-------')
  titles =[]
  for result in news:
    try:
    # Identify and return title of listing
      title = result.a['href']
      titles.append(title)
    #print(title)
    except Exception as e:
      print(e)


  #title = soup.find_all('div', class_='content_title')
  ##print('-------News Title_______')
  string_1 = str(titles[0])
  string_2 = string_1.split('/')
  string_3 = string_2[3].capitalize()
  string_4 = string_3.replace('-',' ')

  soup.find_all(target="_self")
  result_text= soup.find_all('div',class_='rollover_description_inner')[6]

  temp=result_text.find('div',class_='rollover_description_inner')
  news_p = result_text.text

  #news_title = title[1].text

  #print('-'*70)
  #print('-------News_______')
  #print(news_p)
  #print('-'*70)



  url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
  browser.visit(url)
  html = browser.html
  soup = BeautifulSoup(html, 'html.parser')


  image_track = soup.find_all('div',class_='carousel_items')
  string1 = str(image_track)
  strings = string1.split('spaceimages')
  string2=strings[1].split('jpg')[0]

  featured_image_url = 'https://www.jpl.nasa.gov'+'/spaceimages' + string2+ 'jpg'
  #print('------Featured image Url-------')
  #print("featured image url:",featured_image_url)
  #print('-'*70)


# In[187]:


  url = 'https://twitter.com/marswxreport?lang=en'
  browser.visit(url)
  html = browser.html


# In[222]:


  soup = BeautifulSoup(html, 'html.parser')
  results = soup.find_all('span', class_= "css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")

  weather='Weather information is not available'
  for result in results:
    # Error handling
    try:
        weather =result.span(class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    except Exception as e:
        print(e)
        
  print(weather)
  #print('-'*70)
  #print('Mars weather:')
  #print(str_mars_weather[0])
  #print('-'*70)



  facts_url = 'https://space-facts.com/mars/'
  facts_tables = pd.read_html(facts_url)
  facts_df=facts_tables[0]
  facts_df.columns = ["Parameter", "Value"]
  facts_df_new=facts_df.set_index('Parameter')

# In[240]:


  facts_html_table = facts_df_new.to_html()
  #print(facts_html_table)


# In[264]:


  image1 = {
    "title" : "Valles Marineris Hemisphere",
    "img_url" : "https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"
    }

  image2 = {
    "title" : "Cerberus Hemisphere",
    "img_url" : "https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"
  }

  image3 = {
    "title" : "Schiaparelli Hemisphere",
    "img_url" : "https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"
  }

  image4 = {
    "title" : "Syrtis Major Hemisphere",
    "img_url" : "https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"
  }

  images = {
    "image1" : image1,
  "image2" : image2,
    "image3" : image3,
    "image4" : image4
  }

  hemisphere_image_urls = list(images.values())
  #print(hemisphere_image_urls)


# In[265]:
  out = {
    'news_title':string_4,
    'news_p':news_p,
    'featured_image_url':featured_image_url,
    'mars_weather': weather,
    'mars_facts':facts_html_table,
    'image_urls':hemisphere_image_urls
  }

  #print(out)
  return out
