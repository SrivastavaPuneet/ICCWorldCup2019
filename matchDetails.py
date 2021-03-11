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

# selenium driver initialization
driver = webdriver.Chrome('/Users/puneet/Downloads/chromedriver')

# selenium driver options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--no-startup-window')


scorecardList = []  # initializing list of dictionary

for link in allScorecards:
    # dynamically storing scorecard links to a variable
    page = 'https://www.espncricinfo.com' + link['href']
    driver.get(page)  # GET response from selenium driver
    # parsing the text as html source code
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # storing all divs containing match details/facts
    MatchDetails = soup.find_all(
        "div", attrs={"class": "match-page-wrapper scorecard-page-wrapper"})

    # here we are creating a list of dictionaries where
    # each dictionary contains match facts for each match.
    # so a total of 48 dictionaries at the end of all iterations.
    for match in MatchDetails:
        MatchDetailsDict = {}

        # match number
        MatchDetailsDict['Match Number'] = match.find("div", attrs={
                                                      "class": "match-info match-info-MATCH"}).find("div", attrs={"class": "description"}).get_text().split(',')[0].replace(" (D/N)", "")

        # PLAYER OF THE MATCH, PLAYER IMAGE URL, PLAYER COUNTRY
        if match.find("div", attrs={"class": "best-player-name"}):
            MatchDetailsDict['Player of the Match'] = match.find(
                "div", attrs={"class": "best-player-name"}).get_text()
            MatchDetailsDict['POM Image URL'] = match.find(
                "div", attrs={"class": "best-player-content"}).find("img")["src"]
            MatchDetailsDict['POM Country'] = match.find(
                "span", attrs={"class": "best-player-team-name"}).get_text()
        else:
            # if the match had no winner then all "Player of the Match" details remains null
            MatchDetailsDict['Player of the Match'] = np.nan
            MatchDetailsDict['POM Image URL'] = np.nan
            MatchDetailsDict['POM Country'] = np.nan

        # fetching all batsman names from both innings, in a list
        batsmen = [batsman.get_text().split('\xa0')[0]
                   for batsman in match.select("td.batsman-cell")]

        # fetching runs scored by each batsmen in both innings, in a list
        runs = [run.get_text()
                for run in match.select("td[class='font-weight-bold']")]

        # fetching all batting stats including runs, balls, minutes played, 4s, 6s, strike-rate
        battingStats = [element.get_text() for element in
                        [j for sub in
                         [tr.find_all("td", attrs={"class": None, "colspan": None})
                          for tr in match.find_all("table", attrs={"class": "table batsman"})]
                         for j in sub]]
        # extracting "balls played" from batting stats
        bowls = [battingStats[i]
                 for i in range(len(battingStats)) if i % 5 == 0]

        # extracting "strike-rates" from batting stats
        strRates = [battingStats[i]
                    for i in range(len(battingStats)) if i % 5 == 4]

        # runs scored by every batsman
        MatchDetailsDict['Runs by each Batsman'] = ', '.join(
            [(' '.join([batsman, ':', run])) for batsman, run in zip(batsmen, runs)])
        # balls faced by every batsman
        MatchDetailsDict['Bowls faced by each Batsman'] = ', '.join(
            [(' '.join([batsman, ':', bowl])) for batsman, bowl in zip(batsmen, bowls)])
        # strike rate for every batsman
        MatchDetailsDict['Strike Rate of each Batsman'] = ', '.join(
            [(' '.join([batsman, ':', strRate])) for batsman, strRate in zip(batsmen, strRates)])

        # fetching all bowler names from both innings, in a list
        bowlers = [bowler.get_text().split('\xa0')[0]
                   for bowler in match.select("td.text-nowrap")]

        # fetching all bowling stats including overs, runs conceded, wickets, economy-rates, etc
        bowlingStats = [element.get_text() for element in
                        [j for sub in
                         [tr.find_all("td", attrs={"class": None, "colspan": None})
                          for tr in match.find_all("table", attrs={"class": "table bowler"})]
                         for j in sub]]
        # extracting "wickets taken" from bowling stats
        wickets = [bowlingStats[i]
                   for i in range(len(bowlingStats)) if i % 10 == 3]

        # extracting "economy rates" from bowling stats
        ecoRates = [bowlingStats[i]
                    for i in range(len(bowlingStats)) if i % 10 == 4]

        # wickets taken by each bowler
        MatchDetailsDict['Wickets by each Bowler'] = ', '.join(
            [(' '.join([bowler, ':', wicket])) for bowler, wicket in zip(bowlers, wickets)])
        # economy rate for every bowler
        MatchDetailsDict['Economy Rate of each Bowler'] = ', '.join(
            [(' '.join([bowler, ':', ecoRate])) for bowler, ecoRate in zip(bowlers, ecoRates)])
        # which country won the toss
        MatchDetailsDict['Toss'] = match.find("table", attrs={"class": "w-100 table match-details-table"}).find(
            "td", attrs={"class": None}).get_text().replace(u'\xa0', u' ')
        # who were the umpires
        MatchDetailsDict['Umpires'] = ', '.join([umpire.get_text() for umpire in match.find_all(
            "div", attrs={"class": "section-header border-bottom small p-0 player-details"})[-5:][:2]])
        # who was the match referee
        MatchDetailsDict['Match Referee'] = match.find_all("div", attrs={
                                                           "class": "section-header border-bottom small p-0 player-details"})[-1].get_text()

    # adding the data dictionary to the list
    scorecardList.append(MatchDetailsDict)
driver.quit()  # exiting the selenium instance and closing the web browser

print("--- %s seconds ---" % (time.time() - start_time))

# create a dataframe with that list of dictionaries
df = pd.DataFrame(scorecardList)

# user defined function to encode image url links


def hyperlinkEncoding(link, encoding):
    if str(link) == 'nan':
        return 'NA'
    else:
        return ("=HYPERLINK(\"" + str(link) + "\",\"" + str(encoding) + "\")")


# hyperlink encoding for image URL, calling hyperlinkEncoding() function
df['POM Image URL'] = df.apply(lambda x: hyperlinkEncoding(
    x['POM Image URL'], x['Player of the Match']), axis=1)

df.to_csv('matchDetails.tsv', sep='\t', index=False)
