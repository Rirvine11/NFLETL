from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
import pymongo
from splinter import Browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    stats = {}

    receivingURL = 'https://nextgenstats.nfl.com/stats/receiving#yards'
    browser.visit(receivingURL)
    html = browser.html
    soup = bs(html, 'html.parser')

    receivingtable=pd.read_html(str(soup.find_all('table')))
    recdf= pd.DataFrame(receivingtable[1])
    reccolumnlist = receivingtable[0].values.tolist()[0]
    reccolumnlist.pop()
    for i in reccolumnlist:
        i.replace('.','')
    recdf.columns = reccolumnlist
    recdf = recdf.rename(index=str, columns={"+/-Avg .YAC Above Expectation":"+/-Avg YAC Above Expectation"})
    recdf_dict = recdf.to_dict(orient='records')

    rushingURL = 'https://nextgenstats.nfl.com/stats/rushing#yards'
    browser.visit(rushingURL)
    html = browser.html
    soup = bs(html, 'html.parser')

    rushingtable=pd.read_html(str(soup.find_all('table')))
    rushdf= pd.DataFrame(rushingtable[1])
    rushcolumnlist = rushingtable[0].values.tolist()[0]
    rushcolumnlist.pop()
    rushdf.columns = rushcolumnlist
    rushdf_dict = rushdf.to_dict(orient='records')
    
    passingURL = 'https://nextgenstats.nfl.com/stats/passing#yards'
    browser.visit(passingURL)
    html = browser.html
    soup = bs(html, 'html.parser')

    passingtable=pd.read_html(str(soup.find_all('table')))
    passdf= pd.DataFrame(passingtable[1])
    passcolumnlist = passingtable[0].values.tolist()[0]
    passcolumnlist.pop()
    passdf.columns = passcolumnlist
    passdf_dict = passdf.to_dict(orient='records')



    return passdf_dict, rushdf_dict, recdf_dict