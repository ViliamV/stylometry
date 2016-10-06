#!/usr/bin/env python
import tweepy #https://github.com/tweepy/tweepy
import csv
import pickle
# initialize 
tweets = []
tweet_picke = []

def clean_tweet(full_tweet):
    global tweets
    global tweet_picke
    tweet = full_tweet.text.strip().split()
    new_tweet = []
    for word in tweet:
        if word.find('#') !=-1 or word.find('@') !=-1 or word.find('www')!=-1 or word.find('http')!=-1 or word.find('.cz')!=-1 or word.find('.com')!=-1:
            pass
        else:
            new_tweet.append(word)
    tweet = ' '.join(new_tweet) 
    tweets.append(tweet)    
    tweet_picke.append((tweet)))
    


def get_all_tweets(screen_name):
    global tweets
    global tweet_picke
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print("...%s tweets downloaded so far" % (len(alltweets)))
    
    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets = []
    for tweet in alltweets: 
        if not tweet.text.startswith('RT'): 
            clean_tweet(tweet)    
    with open('%s_tweets.txt' % screen_name, 'w') as f:
        for tweet in tweets:
            if tweet != '':
                f.write('{}\n'.format(tweet))    
    pickle.dump(tweet_picke, open('{}.p'.format(screen_name), 'wb'))
 

if __name__ == '__main__':
    #read twitter credentials
    with open('01-twitter-API.txt', 'r') as credentials:
        for line in credentials:
            tag, placeholder, data = line.strip().split(' ')
            if tag == 'consumer_key':
                consumer_key = data
            elif tag == 'consumer_secret':
                consumer_secret = data
            elif tag == 'access_key':
                access_key = data
            elif tag == 'access_secret':
                access_secret = data
    with open('02-mena.txt', 'r') as f:
        for meno in f:
            get_all_tweets(meno.strip())    
