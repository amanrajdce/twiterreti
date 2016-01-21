# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import datetime
import calendar
import sys
# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = 'insert here'
ACCESS_SECRET = 'insert here'
CONSUMER_KEY = 'insert here'
CONSUMER_SECRET = 'insert here'

def print_help():
    print '''Usage: ./get_tweets.py username'''
def get_tweets(user_name):
    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    # Initiate the connection to Twitter REST API
    twitter = Twitter(auth=oauth)
    # Get a particular user's timeline (up to 3,200 of his/her most recent tweets)
    tweets = twitter.statuses.user_timeline(screen_name=str(user_name),count=200)
    print 'number of tweets obtained:',len(tweets)

    # Dumps the json
    with open('tweets_'+str(user_name)+'.json', 'w') as fWrite:
        # write tweets to file one per line
        for tweet in tweets:
            tweetID   = long(tweet['id'])
            tweetTime = tweet['created_at']
            # convert Twitter datetime to unixtime in seconds since 1/1/1970
            strippedTime = datetime.datetime.strptime(tweetTime, '%a %b %d %H:%M:%S +0000 %Y')
            unixTime = calendar.timegm(strippedTime.utctimetuple())
            # write "unixTime \t tweet" to outfile
            writeData = str(unixTime) + '\t' + json.dumps(tweet)
            fWrite.write(unicode(writeData))
            fWrite.write('\n')
        fWrite.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_help()
    else:
        user_name = sys.argv[1]
        get_tweets(user_name)
