from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    #Call the browser function
    browser = init_browser()

    #URL of page to be scraped
    NASA_Mars_url = 'https://mars.nasa.gov/news/'

    #Scraping the Mars News site for latest new's article and it's context
    browser.visit(NASA_Mars_url)
    news_title = browser.find_by_css('.grid_gallery.list_view .content_title').text
    news_p = browser.find_by_css('.article_teaser_body').text

    #Scraping the Mars Space Images - Featured Image
    #Set-up URL and browser
    JPLMarsSpaceImageURL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPLMarsSpaceImageURL)

    #Using splinter to access the page to find the featured image url
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.is_text_present('more info', wait_time=10)
    browser.click_link_by_partial_text('more info')

    #Identify and retrieve the image url needed using the html viewed via splinter browswer
    html = browser.html
    splintersoup = BeautifulSoup(html, 'lxml')
    partOfImageURLS = splintersoup.find('figure', class_='lede').find('a')['href']
    originalURL = "https://www.jpl.nasa.gov"
    featured_image_url = f"{originalURL}{partOfImageURLS}"

    #URL of page to be scraped (Twitter) 
    TwitterMarsWeather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(TwitterMarsWeather)

    #Retrieve the latest Mars Weather
    mars_weather = browser.find_by_css('.tweet').first.find_by_tag('p').text
    
    #Reading and converting an html to a pandas dataframe
    Mars_Facts = "https://space-facts.com/mars/"
    tables = pd.read_html(Mars_Facts)
    df = tables[0]
    df.columns = ["","value"]
    df.set_index("", inplace=True)
    #Converting the dataframe to an html table string
    
    html_table = df.to_html()

    #URL of page to be scraped (Mars Hemispheres)
    MarsHemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(MarsHemispheres)

    #Set-up browser and variables 
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find_all('div', class_='item')
    x = 0
    hemisphere_image_urls = []

    #A loop to go through each hemisphere via Splinter, and obtain the needed title and url image of the hemisphere
    for result in results:
        browser.visit(MarsHemispheres)
        browser.find_by_tag('h3')[x].click()
        
        html_inside_loop = browser.html
        loop_soup = BeautifulSoup(html_inside_loop, 'lxml')
        title = browser.find_by_css('.title').text
        
        part_of_url = loop_soup.find('img', class_='wide-image')['src']
        MarsHemispheres_url = 'https://astrogeology.usgs.gov'
        image_url = f"{MarsHemispheres_url}{part_of_url}"
        hemisphere_image_url = {
            'title': title,
            'img_url': image_url
            }

        hemisphere_image_urls.append(hemisphere_image_url)
        x = x + 1
    #Storing data in a dictionary
    Mars_data = {
        "Title": news_title, 
        "Content":news_p,  
        "Featured_Mars_Image": featured_image_url,
        "Mars_Weather": mars_weather,
        "Mars_Facts": html_table,
        "Mars_Hemispheres": hemisphere_image_urls
    }
    #Close the browser after scraping
    browser.quit()

    #Return results
    return Mars_data