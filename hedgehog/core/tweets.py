import tweepy
import core.keys as keys



auth = tweepy.OAuthHandler(keys.TWITTER_APP_KEY, keys.TWITTER_APP_SECRET)
auth.set_access_token(keys.TWITTER_KEY, keys.TWITTER_SECRET)

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
