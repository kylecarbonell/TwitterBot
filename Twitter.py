import configparser
from re import T
import tweepy
import pandas as pd

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

        self.notAllowed = {"’" : "'", "🎉" : ""}


    def get_tweet(self, name):
        tweets = self.api.user_timeline(screen_name =name, count=1, tweet_mode='extended')
        #columns = ['User', 'Text', 'Time Created']
        data = []
        for tweet in tweets:
            data.append(tweet.full_text)

        msg = "".join(data)
        for char in self.notAllowed:
            msg = msg.replace(char , self.notAllowed[char])
        
        return msg

    def get_news(self):
        tweets = self.api.user_timeline(screen_name ='CNN', count=5)
        columns = ['User', 'Text', 'Time Created']
        data = []
        for tweet in tweets:
            data.append([tweet.user.screen_name, tweet.text, tweet.created_at])

        df = pd.DataFrame(data, columns=columns)
        print(df)

