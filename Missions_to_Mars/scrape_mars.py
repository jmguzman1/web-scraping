#!/usr/bin/env python
# coding: utf-8


# In[34]:


from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

def init_browser(): 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser1 = Browser('chrome', **executable_path, headless=False)
    return browser1

browser = init_browser()

def scrape():
    mars_dict = {}

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)



    html = browser.html
    news_soup = bs(html, 'html.parser')


    # ### NASA Mars News



    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_par = news_soup.find_all('div', class_='article_teaser_body')[0].text



    # ## JPL Mars Space Images - Featured Image

    # In[14]:


    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)


    image_soup = bs(html, 'html.parser')

    image_path = image_soup.find_all('img')[3]["src"]
    featured_image_url = images_url + image_path
    print(featured_image_url)


    # ### Mars Facts



    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    tables

    mars_facts_df = tables[2]
    mars_facts_df.columns
    mars_facts_df


    html_table = mars_facts_df.to_html()
    html_table



    html_table.replace('\n', '')


    # ### Mars Hemispheres


    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html


    soup = bs(html, "html.parser")

    hemisphere_image_urls = []

    imgs = soup.find("div", class_ = "result-list" )
    hemispheres = imgs.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        img = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + img   
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    mars_dict = {
        "news_title": news_title,
        "news_par": news_par,
        "featured_image_url": featured_image_url,
        "mars_facts": str(html_table),
        "hemisphere_images": hemisphere_image_urls}
    return mars_dict


