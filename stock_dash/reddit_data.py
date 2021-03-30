import pandas as pd
import praw
import os

r_cid = os.getenv('reddit_api')
r_csec = os.getenv('reddit_api_sec')
r_uag = os.getenv('reddit_user')


def get_reddit(cid= r_cid, csec= r_csec, uag= r_uag, subreddit='wallstreetbets'):
   
    #connect to reddit
    reddit = praw.Reddit(client_id= cid, client_secret= csec, user_agent= uag)
    #get the new reddit posts
    posts = reddit.subreddit(subreddit).hot(limit=100)
    #load the posts into a pandas dataframe
    p = []
    for post in posts:
        p.append([post.title, post.score, post.url])
    posts_df = pd.DataFrame(p,columns=['title', 'score', 'url'])
    
    return posts_df
