import pandas as pd
import praw
import os
import sqlite3

r_cid = os.getenv('reddit_api')
r_csec = os.getenv('reddit_api_sec')
r_uag = os.getenv('reddit_user')


def get_reddit(cid= r_cid, csec= r_csec, uag= r_uag, subreddit='wallstreetbets'):
    #connect to sqlite database
    conn = sqlite3.connect('stocks.sqlite')
                           
    #connect to reddit
    reddit = praw.Reddit(client_id= cid, client_secret= csec, user_agent= uag)
    #get the new reddit posts
    posts = reddit.subreddit(subreddit).top('day', limit=100)
                           
    #load the posts into a pandas dataframe
    p = []
    for post in posts:
        if post.selftext != "":
            p.append([post.title, post.score, post.selftext])
        else:
            p.append([post.title, post.score, post.url])
                           
    #create dataframe from list
    posts_df = pd.DataFrame(p,columns=['title', 'score', 'post'])
                           
    #save top posts to sqlite database
    posts_df.to_sql('reddit', conn, if_exists = 'replace')
    
    return print('done')
