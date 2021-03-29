# ICCWorldCup2019
This repository contains clean and well collated data for ICC World Cup 2019.

----------------------------------------------------------------------------------------------------------------

From this page: https://www.espncricinfo.com/series/icc-cricket-world-cup-2019-1144415/match-results, following information is scraped:
1. Match number
2. Location
3. Date
4. Winning country
5. Other country
6. Match result
7. Score by winning country
8. Score by other country
9. Link to match report
10. Link to match summary
11. Link to match scorecard

results in a file matchResults.tsv 

.py file as matchResults.py

----------------------------------------------------------------------------------------------------------------

Using each match's scorecard link like https://www.espncricinfo.com/series/icc-cricket-world-cup-2019-1144415/india-vs-new-zealand-1st-semi-final-1144528/full-scorecard following information is extracted:
1. Player of the match with the picture.
2. Country that the player of the match belongs to.
3. Runs scored by every batsman. 
4. Balls played by every batsman.
5. Strike rate for every batsman.
6. Wickets taken by every bowler.
7. Economy rate for every bowler.
8. which country won the toss.
9. who were the umpires?
10. who was the match referee

results in a file matchDetails.tsv. 

.py file as matchDetails.py. 

----------------------------------------------------------------------------------------------------------------

For each player across all matches (using the player page like https://www.espncricinfo.com/newzealand/content/player/506612.html) following is extracted:
1. Full name of player.
2. Date and place of birth.
3. Current age.
4. Major teams.
5. Playing role.
5. Batting style.
6. Bowling style.
7. Highest ODI batting score.
8. ODI debut information.
9. Profile information.
10. Pic of the player. Save the url of the image in the tsv. 
11. Country of the player.

results in a file playerDetails.tsv. 

.py file as playerDetails.py. 
