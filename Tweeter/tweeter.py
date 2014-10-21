__author__ = 'graham'
import tweepy

def main():
    tweet('test')

# 'post' is the tweet contents
# Add keys to twitter account in Twitter_auth_file.txt and put in directory of script calling this def
def tweet(post):
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
    api.update_status(post)
    postsize = len(post)
    print "[bot] Posted: \n" + post
    print "[bot] Length: " + str(postsize)

if __name__ == '__main__':
    main()