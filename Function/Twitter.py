import configparser
import tweepy

class Tweet:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('Data/config.ini')

        #Get keys from config.ini
        api_key = config['twitter']['api_key']
        api_key_secret = config['twitter']['api_key_secret']

        access_token = config['twitter']['access_token']
        access_token_secret = config['twitter']['access_token_secret']
        
        #Authentication
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def get_tweet(self, name: str) -> tuple:
        '''
        This is returns the most recent tweet from the given name. If the tweet 
        contains an image, it will also return the link to the image

        @param name: Name of the twitter user
        '''
        try:
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
        except: 
            return [None, None]
        



