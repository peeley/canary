import pandas as df
import matplotlib.pyplot as plt

tweetframe = df.read_csv('data.csv')

print(tweetframe['Time Posted'])


