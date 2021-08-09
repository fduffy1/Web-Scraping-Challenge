import os
import requests
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from splinter import Browser


def init_browser():
    # splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    url="https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div',class_='content_title').text
    news_p = soup.find('div',class_='article_teaser_body').text
    # create mars_data dict that we can insert into mongo
    mars_data = {
        "news_title":news_title,
        "news_p":news_p,
        "featured":featured(browser),
        "marsfacts":marsfacts(),
        "hemispheres":hemispheres(browser)
    }

    browser.quit()
    return mars_data

def featured (browser):
    browser.visit("https://spaceimages-mars.com")
    browser.find_by_css("a.showimg button").click()
    return browser.find_by_css("img.fancybox-image")["src"]

def marsfacts():
    factsurl = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(factsurl)[0]
    headers = tables.iloc[0]
    df = pd.DataFrame(tables.values[1:],columns=headers)
    df.set_index("Mars - Earth Comparison",inplace=True)
    return df.to_html()

def hemispheres(browser):
    hemispheres = []
    browser.visit("https://marshemispheres.com/")
    thumbnailnumber = len(browser.find_by_css("a.product-item img"))
    for num in range(thumbnailnumber):
        browser.visit("https://marshemispheres.com/")
        browser.find_by_css("a.product-item img")[num].click()
        temp = {}
        temp["title"] = browser.find_by_css("h2.title").first.text
        temp["image"] = browser.find_by_text("Sample").first["href"]
        hemispheres.append(temp)
    return hemispheres

if __name__ == "__main__":
    print(scrape())