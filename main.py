import tweepy, csv, scrape, train

brain = train.Trainer(csvFile='data.csv', stateSize = 2)
tweetwriter = csv.writer(open(brain.csvFile, 'a'), delimiter=',')
crawl = scrape.Crawler()
#crawl.crawlTimeline(tweetwriter)
brain.initializeModel()
#for i in range(0,5):
#	crawl.api.update_status(status = brain.generateTweet())

class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		print("STREAM POST")
		brain.addToModel(status.text)
		crawl.process(status, tweetwriter)
		crawl.api.update_status(brain.generateTweet())
	def on_error(self):
		print("STREAM ERROR")
	def on_timeout(self):
		print("STREAM TIMEOUT")

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = crawl.api.auth, listener = myStreamListener)
print("LISTENING TO STREAM")
myStream.filter(follow=str(crawl.api.get_user(crawl.user_id).id))

