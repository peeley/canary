'''
	main.py
	Noah Snelson
	Main file in canary project responsbile for launching bot and posting
	statuses generated by Trainer based upon scraped text and post times.
'''
import  scrape, train, tweepy, csv, datetime, numpy, time
from datetime import datetime

fileName = 'data.csv'
crawl = scrape.Crawler()

brain = train.Trainer(csvFile=fileName)
brain.generateTimes()

while True :
	now = datetime.now()
	nowMinutes = (now.hour*60)+now.minute
	if(nowMinutes % 5 ==0):
	# prints current time every 5 mins
		print('CURRENT TIME (mins, standard): %i, %s' % (nowMinutes, str(now)))

	# if current time matches schedules post time, post tweet
	if(str(nowMinutes) in brain.postTimes):
		postText = brain.generateTweet()
		print('POSTING TWEET: \n\t' + postText)
		crawl.api.update_status(postText)
		print('POST SUCCESS\n')
	
	# scrapes new tweets and generates new times every day at midnight
	if(nowMinutes == 0):
		with open(fileName, 'w' ) as writer:
			tweetWriter = csv.writer(writer, delimiter=',')
			crawl.crawlTimeline(tweetWriter)
			brain.initializeModel()
			brain.generateTimes()
	time.sleep(60)


