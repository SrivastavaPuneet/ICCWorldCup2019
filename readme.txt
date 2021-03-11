GROUP # 27- DATA COLLECTION ASSIGNMENT README

PUNEET SRIVASTAVA - 12020026
KAIVAN LILAOONWALA - 12020027
ASWIN NARAYANAN - 12020030

Tools used: Selenium and BeautifulSoup


GROUP27_matchResults.py :

Here we are scraping the detailed information about matches from the link provided and creating a .tsv file which provides among other things:
link to match report
ink to match summary
link to match scorecard


Initially we were seeing the complete winning/other country (team) names from the website. However, when we ran the scripts a final time, we noticed the names were coming in abbreviated form (Pakistan:PAK). Hence, we created a dictionary to map the full names


Line # 46-53 in code file
In case of match tied / abandoned without a ball bowled / no result, we have ordered/sorted the teams into 2 columns ("winning team" and "other team") based on the order of their occurrence in the source code
The names of the teams have been put in UPPERCASE (in the output) to draw your attention to the same [For e.g. the FINAL match between New Zealand and England (first record of the output i.e. row 2 in excel sheet)]


Line # 60-69 in code file
In case of match tied / abandoned without a ball bowled / no result, if there is no score against any of the teams, then the score in the excel output has been kept blank/null
[For e.g. the match between India and England (i.e. row 32 in excel sheet)]


The hyperlink encoding for scorecard, match-report and match-summary have been done using a user-defined function: hyperlinkEncoding() function


Output file is GROUP27_matchResults.tsv




GROUP27_matchDetails.py :

Here we are scraping the scorecard link and preparing a summary of player facts/statistics for all matches listed, as well as other match details.

We need to fetch image urls from dynamically loaded pages. Since beautifulsoup cannot fetch certain dynamically loaded components, we have used Selenium for fetching the data from dynamically loaded scorecard pages

Thereafter, we use beautifulsoup - we create a dictionary for each match and its details. This is put into a list and then that is converted into a dataframe.

The format of the all the player-wise stats are as follows (Player name: Runs,) - David Warner : 16, Aaron Finch : 8, Usman Khawaja : 88, Steven Smith : 5


Output file is GROUP27_matchDetails.tsv




GROUP27_playerDetails.py :

Here, we have captured data of players across all the matches played by them. The details cover the profile information and the player pictures.

From the match results page, we have navigated to each scorecard page and fetched the profile information page URLs for each player using beautifulsoup.
The details for each player were fetched using Selenium by navigating dynamically to each profile page.

Any empty cell in the output file is due to the fact that information does not exist.


Output file is GROUP27_playerDetails.tsv

									

									  ~ And that's that. ~