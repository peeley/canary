import tweepy, csv, time
from datetime import datetime

# intializes Crawler as api object using keys from app registration, and initializes variables
class Crawler:
	def __init__(self):
		self.api = tweepy.API(self.authenticate())
		self.user_id = 'realDonaldTrump'
		self.user_posts = self.api.get_user(id=self.user_id).statuses_count
		self.tweets = 0 	
		print("CRAWLER INIT")		
	def authenticate(self):
		print("CRAWLER AUTH")
		consumer_key = 'm8RtmPGMWXLOYbSevMwMCxdWQ'
		consumer_secret = 'cEnIQGj9yBHvxl6X5Rb8ZekKNoliMk1Eb3H71rp9hE2WzEQ4MB'
		access_token = '956820311000969216-BRXHvw9JEJ3TROnPv9UzF2gnLfnzz3r'
		access_token_secret = 'zhAcG95RmKwOITjNfFFucStW9aRrdzYVaAiLKYFesIUPb'	
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		return auth
	# stores tweet id, text, and time posted in csv, prints to console
	def process(self, status, writer): 
		tweet = self.api.get_status(status.id, tweet_mode='extended')
		tweet_text = self.trim(tweet._json['full_text'])
		tweet_time = tweet.created_at
		#writes to csv if tweet is not retweet
		if(not (tweet_text[:2] == 'RT')):
			writer.writerow([tweet.id, tweet_text,tweet_time])	
			print('\t%s -Tweet #%i, ID:%s\n' % (str(tweet_time), self.tweets, str(tweet.id)))
		self.tweets += 1
	
	# trims artifacts of HTML parsing out of tweet text
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
		
	#crawls timeline- after first iteration through timeline, uses max_id
	def crawlTimeline(self):	
		print("CRAWLING TIMELINE")
		tweetfile = open('data.csv', 'w')
		tweetwriter = csv.writer(tweetfile, delimiter=',')
		tweetwriter.writerow(['ID','Text','Time Posted'])
		count = 0
		if count < 3200:
			try:
				for status in tweepy.Cursor(self.api.user_timeline,id=self.user_id).items():	
					self.process(status, tweetwriter)
			# if API encounter rate limit, waits for 1 minute
			except tweepy.RateLimitError:
				print('rate limit error! waiting from \t'+ str(datetime.now()))
				time.sleep(60)
		tweetfile.close()

