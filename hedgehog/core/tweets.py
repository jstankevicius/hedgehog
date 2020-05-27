import tweepy


TWITTER_APP_KEY = "K6FUAS27AcSkXrzckLgl3I75d"
TWITTER_APP_SECRET = "qyVpQnLaltzBWuMs9OSBXybfeH0aNlwsa4OxrAE4UujC9d1TpH"
TWITTER_KEY = "1258887752822726656-bfDDIelsgWwtiquPmVcz41yVCtK6J0"
TWITTER_SECRET = "OdZd2GmqC1aiqYu0IfnBL0bK6XvOcCMUsSEh9rY2aBrHn"

auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)

api = tweepy.API(auth)


class TweetListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status):        
        if status == 420:
            return False

tweet_listener = TweetListener()
stream = tweepy.Stream(auth=api.auth, listener=tweet_listener)
stream.filter(track=["bitcoin"])
