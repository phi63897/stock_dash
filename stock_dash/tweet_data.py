import tweepy
import pandas as pd
import sqlite3
import json
import os
import datetime
from datetime import date
import texthero as hero
import regex as re
import string

#import twitter api keys
t_conkey = os.getenv('twitter_api')
t_consec = os.getenv('twitter_api_sec')
t_akey = os.getenv('twitter_access')
t_asec = os.getenv('twitter_access_sec')

def get_all_tweets(screen_name
                   ,consumer_key = t_conkey
                   , consumer_secret= t_consec
                   , access_key= t_akey
                   , access_secret=  t_asec
                   ):
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
               
    #all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
           
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    tweets_df = pd.DataFrame(outtweets, columns = ['time', 'datetime', 'text'])

    return tweets_df



def get_options_flow():
 
    #connect to the sqlite database
    conn = sqlite3.connect('stocks.sqlite')
    
    #use get_all_tweets to pull the data from the twitter users
    ss = get_all_tweets(screen_name ="SwaggyStocks")
    uw = get_all_tweets(screen_name ="unusual_whales")
    
    #clean the text data
    ss['source'] = 'swaggyStocks'
    ss['text'] = hero.remove_urls(ss['text'])
    ss['text'] = [n.replace('$','') for n in ss['text']]
    
    #clean the text data
    uw['source'] = 'unusual_whales'
    uw['text'] = hero.remove_urls(uw['text'])
    uw['text'] = [n.replace('$','') for n in uw['text']]
    uw['text'] = [n.replace(':','') for n in uw['text']]
    uw['text'] = [n.replace('\n',' ') for n in uw['text']]
    uw['text'] = [n.replace('  ',' ') for n in uw['text']]
    
    #concat the tweets into one dataframe    
    tweets = pd.concat([ss, uw])
    #save the tweets to sqlite database
    tweets.to_sql('tweets', conn, if_exists = 'replace')
    return print('done')