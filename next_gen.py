from splinter import Browser
from bs4 import BeautifulSoup

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
    recdf.columns = reccolumnlist

    stats['receiving'] = recdf

    rushingURL = 'https://nextgenstats.nfl.com/stats/rushing#yards'
    browser.visit(rushingURL)
    html = browser.html
    soup = bs(html, 'html.parser')

    rushingtable=pd.read_html(str(soup.find_all('table')))
    rushdf= pd.DataFrame(rushingtable[1])
    rushcolumnlist = rushingtable[0].values.tolist()[0]
    rushcolumnlist.pop()
    rushdf.columns = rushcolumnlist

    stats['rushing'] = rushdf
    
    passingURL = 'https://nextgenstats.nfl.com/stats/passing#yards'
    browser.visit(passingURL)
    html = browser.html
    soup = bs(html, 'html.parser')

    passingtable=pd.read_html(str(soup.find_all('table')))
    passdf= pd.DataFrame(passingtable[1])
    passcolumnlist = passingtable[0].values.tolist()[0]
    passcolumnlist.pop()
    passdf.columns = passcolumnlist

    stats['passing'] = passdf

    return stats