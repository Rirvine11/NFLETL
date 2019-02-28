��# NFLETL

Ryan Irvine
Nick Donahoe

A database of all possible data on NFL players. The database provides access to the 2018 NFL season containing the fantasy points for each elgible player. Data was pulled from https://api.fantasy.nfl.com/ for the fantasy data for each week. Webscraping was utilized to collect data from https://nextgenstats.nfl.com/ collect the advanced stats for rushing, receiving, and passing stats. Lastly, we downloaded a csv containing information regarding the NFL schedule per week and location and time the game was played. All data was passed into a mongo database using flask where the data can queryed to find the information the user desires. 
