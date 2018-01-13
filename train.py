import pandas as pd
# import matplotlib
# from  matplotlib import pyplot as plt
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

# importing data frame
tweetframe = pd.read_csv('data.csv')
text = tweetframe['Text']
print('Data on ' +str(text.count())+' tweets\n')

# configuring markov chain
tweet_models = []
count = 0
for i in text:
	tweet_models.append(markovify.Text(i, state_size = 2 ))
final_model = markovify.combine(models=tweet_models)

# generates tweet, refuses 'None' content
def output(model):
	tweet = str(model.make_sentence())
	if(tweet == 'None ' or tweet == 'None'):
		return(output(model))
	else:
		return tweet

# outputs to CLI
for i in range(0, 10):	
	print(str(output(final_model)) + '\n')
