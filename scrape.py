'''
	scrape.py
	Noah Snelson
	Crawler object responsible for authenticating Twitter API and crawling
	user timeline to store tweet ID, text, and time of posting to specified .csv
'''

import tweepy, csv, time, json
import pandas as pd
from datetime import datetime

# intializes Crawler w/ vars. and as api object using keys from app registration
class Crawler:
	def __init__(self):
		self.api = tweepy.API(self.authenticate())
		self.user_id = 'realDonaldTrump'
		self.user_posts = self.api.get_user(id=self.user_id).statuses_count
		self.tweets = 0
		print("CRAWLER INIT")	

	# authenticates API
	def authenticate(self):
                print("CRAWLER AUTH")
                with open('auth.json') as jsonFile:
                    auth = json.load(jsonFile)
                    consumer_key = auth['consumer_key']
                    consumer_secret = auth['consumer_secret']
                    access_token = auth['access_token']
                    access_token_secret = auth['access_token_secret']	
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                return auth

	# stores tweet id, text, and time posted in csv, prints to console
	def process(self, status, writer): 
		tweet = self.api.get_status(status.id, tweet_mode='extended')
		tweet_text = self.trim(tweet._json['full_text'])
		tweet_time = pd.to_datetime(tweet.created_at, format='%Y-%m-%d %H:%M:%S')
		tweet_time = int((tweet_time.hour * 60) + tweet_time.minute)
		#writes to csv if tweet is not retweet
		if(not (tweet_text[:2] == 'RT')):
			self.tweets += 1
			writer.writerow([tweet.id, tweet_text,tweet_time])
			print(tweet_text)
			print('\tminute posted: %s | tweet #%i | id:%s\n' % (str(tweet_time), self.tweets, str(tweet.id)))
		
	
	# trims escape characters, non-unicode out of tweet text
	def trim(self, str):
		if('http' in str):
			str = str[:str.find('http')]
		if('&amp;' in str):
			str = str.replace('&amp;', 'and')
		if('(' in str):
			str = str.replace('(','-')
		if(')' in str):
			str = str.replace(')','-')
		if('[' in str):
			str = str.replace('[','-')
		if('"' in str):
			str = str.replace('"','')
		if("'" in str):
			str = str.replace("'",'')
		if('”' in str):
			str = str.replace('”','')
		return str
		
	# crawls timeline and writes to csv, terminates crawl when 
	# duplicate tweet is found
	def crawlTimeline(self, writer):	
		print("CRAWLING TIMELINE")
		writer.writerow(['ID','Text','Time Posted'])
		lastTime = 0
		for status in tweepy.Cursor(self.api.user_timeline,id=self.user_id).items():
			try:
				if(status.created_at != lastTime):
					lastTime = status.created_at
					self.process(status, writer)
				else:
					break
			# if api encounter rate limit, waits for 1 minute
			except tweepy.RateLimitError:
				print('rate limit error! waiting from \t'+ str(datetime.now()))
				time.sleep(60)
		
# for debugging, replicate data for backup
if __name__ == '__main__':
	tweetWriter = csv.writer(open('data.csv', 'w'), delimiter=',')
	crawler = Crawler()
	crawler.crawlTimeline(tweetWriter)

