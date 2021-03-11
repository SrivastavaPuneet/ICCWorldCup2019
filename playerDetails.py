# importing revant libraries
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
# for loading javascript components like image and its url
from selenium import webdriver
import time

# page url from which scorecard urls are fetched
homepage = 'https://www.espncricinfo.com/series/icc-cricket-world-cup-2019-1144415/match-results'

response = requests.get(homepage)  # GET response from the defined url
content = response.content  # fetching content from GET response
# parsing the text as html source code
soup = BeautifulSoup(content, "html.parser")

# fetching all tags that contain scorecard urls
allScorecards = soup.find_all(class_="match-info-link-FIXTURES")

start_time = time.time()

scorecardList = []  # initializing list of dictionary
finalSet = set()  # initializing a set, for unique list of players
for link in allScorecards:
    # dynamically storing scorecard links to a variable
    page = 'https://www.espncricinfo.com' + link['href']
    response = requests.get(page)  # GET response
    content = response.content  # fetching content from GET response
    # parsing the text as html source code
    soup = BeautifulSoup(content, "html.parser")

    # storing all divs containing player URLS
    MatchDetails = soup.find_all(
        "div", attrs={"class": "match-page-wrapper scorecard-page-wrapper"})

    # here we create a Set, which would insure a unique count of players(URLs).
    for match in MatchDetails:
        allPlayers = set([player['href']
                          for player in match.select("a[class='small']")[:-1]])

    finalSet.update(allPlayers)
    # finalSet contains the link to player information page for all playerd who played in the World Cup

print("Time taken to fetch link of all players --- %s seconds ---" %
      (time.time() - start_time))

playerDetailsList = []  # initializing list of dictionary

start_time = time.time()

# selenium driver options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--no-startup-window')

# selenium driver initialization
driver = webdriver.Chrome('/Users/puneet/Downloads/chromedriver')
# here we dynamically visit each player-info page and get required information.
# dynamically navigating to player-info pages is done using Selenium as we need to fetch some dynamically loaded information like player image URL
for playerlink in finalSet:

    driver.get(playerlink)
    playerSoup = BeautifulSoup(driver.page_source, 'html.parser')
    playerDetails = playerSoup.find("div", attrs={"id": "ciHomeContentlhs"})

    playerDetailsDict = {}  # initalizing a dictionary to save player details

    # Full Name of the player
    playerDetailsDict['Player'] = playerDetails.find("div", attrs={
                                                     "style": "margin:0; float:left; padding-bottom:3px;"}).find("h1").get_text().split('\xa0')[0]
    playerDetailsDict['Full Name'] = ''.join([stat.find("span").get_text() for stat in playerDetails.find("div", attrs={
                                             "style": "float:left; width:310px; color:#666666; font-size:11px;"}).find_all("p") if stat.find("b").get_text() == 'Full name'])

    # Date and Place of birth
    playerDetailsDict['Date and Place of Birth'] = ''.join([stat.find("span").get_text() for stat in playerDetails.find("div", attrs={
                                                           "style": "float:left; width:310px; color:#666666; font-size:11px;"}).find_all("p") if stat.find("b").get_text() == 'Born']).replace('\n', '')

    # Current Age
    playerDetailsDict['Current Age'] = ''.join([stat.find("span").get_text() for stat in playerDetails.find("div", attrs={
                                               "style": "float:left; width:310px; color:#666666; font-size:11px;"}).find_all("p") if stat.find("b").get_text() == 'Current age'])

    # Major teams
    playerDetailsDict['Major Teams'] = ''.join([info.text for info in playerDetails.find_all("p", attrs={
                                               "class": "ciPlayerinformationtxt"}) if info.find('b').get_text() == "Major teams"]).replace('Major teams ', '').replace('span', '')

    # playing role
    playerDetailsDict['Playing Role'] = ''.join([stat.find("span").get_text() for stat in playerDetails.find("div", attrs={
                                                "style": "float:left; width:310px; color:#666666; font-size:11px;"}).find_all("p") if stat.find("b").get_text() == 'Playing role'])

    # batting style
    playerDetailsDict['Batting Style'] = ''.join([stat.find("span").get_text() for stat in playerDetails.find("div", attrs={
                                                 "style": "float:left; width:310px; color:#666666; font-size:11px;"}).find_all("p") if stat.find("b").get_text() == 'Batting style'])

    # bowling style
    playerDetailsDict['Bowling Style'] = ''.join([stat.find("span").get_text() for stat in playerDetails.find("div", attrs={
                                                 "style": "float:left; width:310px; color:#666666; font-size:11px;"}).find_all("p") if stat.find("b").get_text() == 'Bowling style'])

    # highest ODI batting score
    playerDetailsDict['Highest ODI Score'] = ''.join([score.find_next_siblings("td")[4].text for score in playerDetails.find(
        "table", attrs={"class": "engineTable"}).find_all("td", attrs={"class": "left"}) if score.text == "ODIs"])

    # ODI debut information
    playerDetailsDict['ODI Debut'] = playerDetails.find_all("table", attrs={"class": "engineTable"})[2].find_all(
        "tr", attrs={"class": "data2"})[2].find("td", attrs={"width": "100%"}).get_text().replace(' scorecard', '')

    # profile information
    playerDetailsDict['Profile Information'] = "\n ".join([profileText.get_text().replace(
        '\n', '') for profileText in playerDetails.find_all("p", attrs={"class": "ciPlayerprofiletext1"})])

    # URL of the picture of the player
    playerDetailsDict['Picture of the Player'] = playerDetails.find(
        "img", attrs={"style": "float:right"})['src']

    # Country of the player
    playerDetailsDict['Country'] = playerDetails.find("div", attrs={
                                                      "style": "margin:0; float:left; padding-bottom:3px;"}).find("b").get_text()

    # adding the data dictionary to the list
    playerDetailsList.append(playerDetailsDict)

driver.quit()  # exiting the selenium instance and closing the web browser

print("Time taken to fetch details of all players --- %s seconds ---" %
      (time.time() - start_time))

df = pd.DataFrame(playerDetailsList)

# user defined function to encode image url links


def hyperlinkEncoding(link, encoding):
    return ("=HYPERLINK(\"" + link + "\",\"" + encoding + "\")")


# hyperlink encoding for image URL, calling hyperlinkEncoding() function
df['Picture of the Player'] = df.apply(lambda x: hyperlinkEncoding(
    x['Picture of the Player'], (x['Player'])), axis=1)

df.to_csv('playerDetails.tsv', sep='\t', index=False)
