# canary
Twitter bot that learns how users tweets through Markov chain. Data is collected by scraping Twitter through Tweepy module,
and Markov model is constructed by using the markovify module. Data is stored locally in a .csv file, and the program schedules
to scrap new data every night at midnight to keep the model up-to-date.
Currently, this is being used for ROBOTRUMP, a bot that learns how to tweet like Donald Trump.
This bot can be found at twitter.com/R0B0TRUMP.
