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
	def __init__(self, csvFile, stateSize):
		self.csvFile = csvFile
		self.data = pd.read_csv(self.csvFile)
		self.times = self.data['Time Posted']
		self.stateSize = stateSize
		self.initializeModel()
		print("TRAINER INIT")

	# generates Markov chain model and fits times to SVM
	def initializeModel(self):
		print('TRAINER BUILDING MODEL')
		tweet_models = []
		for i in self.data['Text']:
			tweet_models.append(markovify.Text(i, self.stateSize))
		self.model = markovify.combine(models=tweet_models)

	# adds single tweet to model and adds time of tweet to SVM
	def addToModel(self, text):
		print('TRAINER ADDING TO MODEL')
		newModel = markovify.Text(text, self.stateSize)
		self.model = markovify.combine(models=[self.model, newModel])

	# generates tweet, refuses 'None' content
	def generateTweet(self):
		print('TRAINER GENERATING TWEET\n')
		tweet = str(self.model.make_sentence())
		if(tweet[:5] == 'None'):
			return(generateTweet(self.model))
		else:
			return tweet

# generates fake tweet and time of tweet
if __name__ == '__main__':
	train = Trainer('data.csv', 2)
	train.initializeModel()
	while True:
		generatedTime = numpy.random.randint(24*60)
		if(generatedTime in train.times[:]):
			print(train.generateTweet())
			print('\tminute to post: %i\n' % (generatedTime))
			time.sleep(2)
