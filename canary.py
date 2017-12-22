import tweepy

consumer_key = 'wFRNosYy0eK6ph2pRIKwMybqe'
consumer_secret = 'HU4N6iBn1NqI3LEx7L6hVYsBZp08WfANwBKnzt9hy97gBBiEjp'
access_token = '1287375775-3x7S7mWHVrXkIc8ZFEemRkVCpjdn5aXbhyxKf9H'
access_token_secret = '0kTiFLNlqcuzjGkBH5rz02caxsVYAUPs6WOaoCrWmmMv5'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

followers = api.friends

the_donald = api.get_user(screen_name='realDonaldTrump')
tweets = 0

for p in range(1, int((the_donald.statuses_count)/20)):
    for i in api.user_timeline(screen_name='realDonaldTrump', page = p):
        tweet = api.get_status(i.id, tweet_mode='extended')
        print (tweet._json['full_text'])
        tweets += 1
        print('\t'+ str(tweet.created_at))
        print('\t'+ str(tweet.coordinates) + '\n')
    print('\t Page %d, w/ %d tweets \n' %  (p, tweets))
print(tweets)
