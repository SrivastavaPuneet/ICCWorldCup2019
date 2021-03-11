#!/usr/bin/env python
# coding: utf-8

# In[27]:


# Data Collection Assignment - Group 27
# Puneet Srivastava - 12020026
# Kaivan Pervez Lilaoonwala -  12020027
# Aswin Narayanan - 12020030


# importing revant libraries
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

# page url from which match results are fetched
page = 'https://www.espncricinfo.com/series/icc-cricket-world-cup-2019-1144415/match-results'

response = requests.get(page)  # GET response from the defined url
content = response.content  # fetching content from GET response

# parsing the text as html source code
soup = BeautifulSoup(content, "html.parser")

# fetching all tags that contains match result info
allGamesSummary = soup.find_all(
    "div", attrs={"class": "match-info match-info-FIXTURES"})

# fetching all tags that contain url links to full-scorecards
allScorecards = soup.find_all(class_="match-info-link-FIXTURES")


# here we are creating a list of dictionaries where
# each dictionary contains result information of each match.
# so a total of 48 dictionaries at the end of all iterations.
MatchList = []
# iterating on a soup containing match-results info and scorecard link
for match, link in zip(allGamesSummary, allScorecards):
    MatchResultsDict = {}

    # match number
    MatchResultsDict['Match Number'] = match.find(
        "div", attrs={"class": "description"}).get_text().split(',')[0].replace(" (D/N)", "")

    # location
    MatchResultsDict['Location'] = match.find(
        "div", attrs={"class": "description"}).get_text().split(',')[1]

    # date
    MatchResultsDict['Date'] = match.find(
        "div", attrs={"class": "description"}).get_text().split(',')[2]

    # winning and other country
    if match.find("div", attrs={"class": "status-text"}).get_text() in ['Match tied', 'Match abandoned without a ball bowled', 'No result']:
        # in case of a match with no result,
        # teams are put in the two given columns based on their order of occurance in the source code.
        MatchResultsDict['Winning Country'] = list(match.find("div", attrs={"class": "teams"}).children)[
            0].find("p", attrs={"class": "name"}).get_text()
        MatchResultsDict['Other Country'] = list(match.find("div", attrs={"class": "teams"}).children)[
            1].find("p", attrs={"class": "name"}).get_text()
    else:
        #         print((match.select('div.team.team-gray')[0].find("p",attrs={"class": "name"}).get_text()))
        MatchResultsDict['Other Country'] = match.select(
            'div.team.team-gray')[0].find("p", attrs={"class": "name"}).get_text()
        MatchResultsDict['Winning Country'] = match.select(
            'div.team:not(.team-gray)')[0].find("p", attrs={"class": "name"}).get_text()

    # match result
    MatchResultsDict['Match Result'] = match.find(
        "div", attrs={"class": "status-text"}).get_text()

    # score by winning country and score by other country
    # if there is no <class = "score"> tag in the source code, the column remains empty
    if match.find("div", attrs={"class": "status-text"}).get_text() in ['Match tied', 'No result', 'Match abandoned without a ball bowled']:
        if list(match.find("div", attrs={"class": "teams"}).children)[0].find("span", attrs={"class": "score"}):
            MatchResultsDict['Score by Winning Country'] = list(match.find("div", attrs={"class": "teams"}).children)[
                0].find("span", attrs={"class": "score"}).get_text().upper()
        else:
            MatchResultsDict['Score by Winning Country'] = np.nan
        if list(match.find("div", attrs={"class": "teams"}).children)[1].find("span", attrs={"class": "score"}):
            MatchResultsDict['Score by Other Country'] = list(match.find("div", attrs={"class": "teams"}).children)[
                1].find("span", attrs={"class": "score"}).get_text().upper()
        else:
            MatchResultsDict['Score by Other Country'] = np.nan
    else:
        MatchResultsDict['Score by Other Country'] = match.select(
            'div.team.team-gray')[0].find("span", attrs={"class": "score"}).get_text()
        MatchResultsDict['Score by Winning Country'] = match.select(
            'div.team:not(.team-gray)')[0].find("span", attrs={"class": "score"}).get_text()

    # link to match report
    MatchResultsDict['Link to Match Report'] = "https://espncricinfo.com" + \
        '/'.join(link['href'].split('/')[:-1]) + '/match-report'

    # link to match summary
    MatchResultsDict['Link to Match Summary'] = "https://espncricinfo.com" + \
        '/'.join(link['href'].split('/')[:-1]) + '/live-cricket-score'

    # link to match scorecard
    MatchResultsDict['Link to Match Scorecard'] = "https://espncricinfo.com" + link['href']

    # adding the data dictionary to the list
    MatchList.append(MatchResultsDict)

# create a dataframe with that list of dictionaries
df = pd.DataFrame(MatchList)

# user defined function to encode url links


def hyperlinkEncoding(link, encoding):
    return ("=HYPERLINK(\"" + link + "\",\"" + encoding + "\")")


# hyperlink encoding for scorecard, match-report and match-summary
df['Link to Match Scorecard'] = df.apply(lambda x: hyperlinkEncoding(x['Link to Match Scorecard'], (
    x['Match Number'] + ' - ' + x['Winning Country'].title() + ' vs ' + x['Other Country'].title())), axis=1)
df['Link to Match Report'] = df.apply(lambda x: hyperlinkEncoding(x['Link to Match Report'], (
    x['Match Number'] + ' - ' + x['Winning Country'].title() + ' vs ' + x['Other Country'].title())), axis=1)
df['Link to Match Summary'] = df.apply(lambda x: hyperlinkEncoding(x['Link to Match Summary'], (
    x['Match Number'] + ' - ' + x['Winning Country'].title() + ' vs ' + x['Other Country'].title())), axis=1)

# dictionary mapping of abbreviated country names to full names
TeamNameMapping = {
    'AUS': 'Australia',
    'ENG': 'England',
    'SL': 'Sri Lanka',
    'SA': 'South Africa',
    'BDESH': 'Bangladesh',
    'WI': 'West Indies',
    'AFG': 'Afghanistan',
    'NZ': 'New Zealand',
    'INDIA': 'India',
    'PAK': 'Pakistan'
}

# replacing abbreviated country names with full names
df = df.replace({"Winning Country": TeamNameMapping})
df = df.replace({"Other Country": TeamNameMapping})


# converting country names to uppercase when no winner
for index, row in df.iterrows():
    if row['Match Result'] in ['Match tied', 'Match abandoned without a ball bowled', 'No result']:
        df.loc[index, 'Winning Country'] = row['Winning Country'].upper()
        df.loc[index, 'Other Country'] = row['Other Country'].upper()


# writing the dataframe in a tsv file
df.to_csv('Group27_matchResults.tsv', sep='\t', index=False)
