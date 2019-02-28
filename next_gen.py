from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
import pymongo
from splinter import Browser
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    receivingURL = 'https://nextgenstats.nfl.com/stats/receiving#yards'
    browser.visit(receivingURL)
    html = browser.html
    soup = bs(html, 'html.parser')

    receivingtable=pd.read_html(str(soup.find_all('table')))
    recdf= pd.DataFrame(receivingtable[1])
    reccolumnlist = receivingtable[0].values.tolist()[0]
    reccolumnlist.pop()
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

    # List of each week number
    weeks = list(range(1,18))
    # Api Url
    base_url = "http://api.fantasy.nfl.com/v1/players/stats?statType=weekStats&season=2018&week={}&form=json"
    temp_final_df = pd.DataFrame()
    for week in weeks:
        target_url = base_url.format(week)
        temp = requests.get(target_url).json()['players']
        temp_df = pd.DataFrame(temp)
        temp_df = temp_df.drop(columns = 'stats')
        temp_df['week'] = week
        temp_final_df = temp_final_df.append(temp_df)
    team_names = temp_final_df.teamAbbr.unique()

    temp_dict = temp_final_df.to_dict(orient='records')

    data = pd.read_csv(r'C:\\Users\\rirvi\Documents\\NFLETL\\2018_Schedule_City.csv')
    data['away_abrev'] = data['Away'].str[0:4]
    data['home_abrev'] = data['Home'].str[0:4]

    away_abrev = []

    for awy in data['away_abrev']:
        away_abrev.append(process.extract(awy,team_names)[0][0])

    home_abrev = []

    for hme in data['home_abrev']:
        home_abrev.append(process.extract(hme,team_names)[0][0])

    data['away_abrev'] = away_abrev
    data['home_abrev'] = home_abrev
    schedule_dict = data.to_dict(orient='records')

    return passdf_dict, rushdf_dict, recdf_dict, temp_dict, schedule_dict

def points():
        # List of each week number
    weeks = list(range(1,18))
    # Api Url
    base_url = "http://api.fantasy.nfl.com/v1/players/stats?statType=weekStats&season=2018&week={}&form=json"
    temp_final_df = pd.DataFrame()
    for week in weeks:
        target_url = base_url.format(week)
        temp = requests.get(target_url).json()['players']
        temp_df = pd.DataFrame(temp)
        temp_df = temp_df.drop(columns = 'stats')
        temp_df['week'] = week
        temp_final_df = temp_final_df.append(temp_df)
    team_names = temp_final_df.teamAbbr.unique()

    temp_dict = temp_final_df.to_dict(orient='records')
    #Schedule
    data = pd.read_csv('./2018_Schedule_City.csv')
    data['away_abrev'] = data['Away'].str[0:4]
    data['home_abrev'] = data['Home'].str[0:4]

    away_abrev = []

    for awy in data['away_abrev']:
        away_abrev.append(process.extract(awy,team_names)[0][0])

    home_abrev = []

    for hme in data['home_abrev']:
        home_abrev.append(process.extract(hme,team_names)[0][0])

    data['away_abrev'] = away_abrev
    data['home_abrev'] = home_abrev
    schedule_dict = data.to_dict(orient='records')
   
    return temp_dict, schedule_dict 