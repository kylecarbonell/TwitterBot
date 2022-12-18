import configparser
from re import T
import tweepy
import pandas as pd
import emoji
import demoji

import json

class Tweet:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')

        #Get keys from config.ini
        api_key = config['twitter']['api_key']
        api_key_secret = config['twitter']['api_key_secret']

        access_token = config['twitter']['access_token']
        access_token_secret = config['twitter']['access_token_secret']
        
        #Authentication
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)



    def get_tweet(self, name):
        tweets = self.api.user_timeline(screen_name =name, count=1, tweet_mode='extended')
        tweet = tweets[0]

        msg = "\n".join(["@" + tweet.user.screen_name + ":", tweet.full_text])
        url = None
        if 'https' in msg:
            msg = msg[0 : msg.index('https')-1]
            if 'media' in tweet.entities:
                for image in tweet.entities['media']:
                    url = (image['media_url'])
        return [msg, url]

    def get_image(self, file):
        pass

    def get_news(self):
        tweets = self.api.user_timeline(screen_name ='CNN', count=5)
        columns = ['User', 'Text', 'Time Created']
        data = []
        for tweet in tweets:
            data.append([tweet.user.screen_name, tweet.text, tweet.created_at])

        df = pd.DataFrame(data, columns=columns)
        print(df)

