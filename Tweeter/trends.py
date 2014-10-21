__author__ = 'graham'
import tweepy
import json

def trending():
    f = open('SydneyRadar.txt')
    lines = f.readlines()
    f.close()
    access_token = lines[0].strip()
    access_token_secret = lines[1].strip()
    consumer_key = lines[2].strip()
    consumer_secret = lines[3].strip()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # The Yahoo! Where On Earth ID for the entire world is 1.
    # See https://dev.twitter.com/docs/api/1.1/get/trends/place and
    # http://developer.yahoo.com/geo/geoplanet/

    WORLD_WOE_ID = 23424748
    # Australia = 23424748
    # World = 0

    # Prefix ID with the underscore for query string parameterization.
    # Without the underscore, the twitter package appends the ID value
    # to the URL itself as a special case keyword argument.

    world_trends = api.trends_place(WORLD_WOE_ID)
    # trends1 is a list with only one element in it, which is a
    # dict which we'll put in data.
    data = world_trends[0]
    # grab the trends
    trends = data['trends']
    # grab the name from each trend
    names = [trend['name'] for trend in trends]
    #for i in names:
    #     print i

    return names



if __name__ == '__main__':
    trending()