import pandas as pd
import markovify
import spacy

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
		frame = pd.read_csv(csvFile)
		self.data = frame['Text']
		self.stateSize = stateSize
		print("TRAINER INIT")

	# generates Markov chain model
	def initializeModel(self):
		print('TRAINER BUILDING MODEL')
		tweet_models = []
		for i in self.data:
			tweet_models.append(markovify.Text(i, self.stateSize ))
		self.model = markovify.combine(models=tweet_models)

	# adds single tweet to model
	def addToModel(self, text):
		print('TRAINER ADDING TO MODEL')
		self.model = markovify.combine(models=[self.model, text])
	# generates tweet, refuses 'None' content
	def generateTweet(self):
		print('TRAINER GENERATING TWEET')
		tweet = str(self.model.make_sentence())
		if(tweet[:5] == 'None'):
			return(generateTweet(self.model))
		else:
			return tweet
