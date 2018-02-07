import tweepy, csv, scrape, train

crawl = scrape.Crawler()
crawl.crawlTimeline()
brain = train.Trainer(csvFile='data.csv', stateSize = 2)
brain.initializeModel()
for i in 5:
	crawl.api.update_status(status = brain.generateTweet())
class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		brain.addToModel(status.text)
		tweetwriter = csv.writer(open(brain.csvFile), delimiter=',')
		crawl.process(status, tweetwriter)
		crawl.api.update_status(brain.generateTweet())

