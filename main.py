import  scrape, train, tweepy, csv, datetime, numpy, time
from datetime import datetime

fileName = 'data.csv'
tweetWriter = csv.writer(open(fileName, 'a'), delimiter=',')
crawl = scrape.Crawler(tweetWriter)
#crawl.crawlTimeline()
brain = train.Trainer(csvFile=fileName, stateSize = 2)


numpy.random.seed(datetime.now().microsecond)
maxPost = 3
postTimes = []
for i in range(maxPost):
	postTimes.append(brain.times[numpy.random.randint(brain.times.shape[0])])
print(postTimes)
while True :
	now = datetime.now()
	nowMinutes = (now.hour*60)+now.minute
	print(nowMinutes)
	if(nowMinutes in postTimes):
		print(brain.generateTweet())
		crawl.update_status(brain.generateTweet)
	if(nowMinutes == 0):
		numpy.random.seed(now.microsecond)
		for i in range(maxPost):
			postTimes.append[brain.times[numpy.random.randint(brian.times.shape[0])]]
		print(postTimes)
	time.sleep(60)


