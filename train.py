'''
	train.py
	Noah Snelson
	Trainer object responsible for constructing model to generate tweets with Markov
	chain based upon data from specified .csv file.
'''

import pandas as pd
from datetime import datetime
import markovify, spacy, numpy, time

# adds natural language processing to tweet generation
nlp = spacy.load('en')
class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

class Trainer():
	# trainer constructor, by default posts 3 times per day and
	# Markov chain has state size of 2
	def __init__(self, csvFile, stateSize=2, maxPosts=3):
		self.csvFile = csvFile
		self.data = pd.read_csv(self.csvFile, engine ='python')
		self.times = self.data['Time Posted']
		self.stateSize = stateSize
		self.maxPosts = maxPosts
		self.initializeModel()
		print("TRAINER INIT")

	# generates Markov chain model and fits times to SVM
	def initializeModel(self):
		print('TRAINER BUILDING MODEL')
		tweet_models = []
		for i in self.data['Text']:
                    tweet_models.append(markovify.Text(str(i), self.stateSize))
		self.model = markovify.combine(models=tweet_models)

	# adds single tweet to model and adds time of tweet to SVM
	def addToModel(self, text):
		print('TRAINER ADDING TO MODEL')
		newModel = markovify.Text(text, self.stateSize)
		self.model = markovify.combine(models=[self.model, newModel])

	# generates tweet, refuses 'None' content by recursive call until non-None content
	def generateTweet(self):
		print('TRAINER GENERATING TWEET...')
		tweet = str(self.model.make_sentence())
		if(tweet[:5] == 'None'):
                    print('TWEET EMPTY, REGENERATING...\n')
                    return(self.generateTweet())
		else:
                    return tweet

	# schedules n post times where n = self.maxPosts based upon previous 
	# post times of user
	def generateTimes(self):
		now = datetime.now()
		numpy.random.seed(now.microsecond)
		self.postTimes = []
		for i in range(self.maxPosts):
			retrievedTime = self.times[numpy.random.randint(self.times.shape[0])]
			self.postTimes.append(str(retrievedTime))
		print('POST TIMES FOR %i-%i\t' % (now.month, now.day))
		print(self.postTimes)

# for debugging, output to console fake tweet and time every 2 seconds
if __name__ == '__main__':
	train = Trainer('data.csv', 2)
	train.initializeModel()
	while True:
		generatedTime = numpy.random.randint(24*60)
		if(generatedTime in train.times[:]):
			print(train.generateTweet())
			print('\tminute to post: %i\n' % (generatedTime))
			time.sleep(2)
