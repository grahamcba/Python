import praw
import tweepy
import time
import datetime
import logging

def strip_title(title):
    if len(title) < 115:
        return title
    else:
        return title[:114] + "..."

def tweet_creator(subreddit_info):
    post_dict = {}
    post_ids = []
    print "[STATUS] Getting posts from Reddit"
    logging.info('[STATUS] Getting posts from Reddit')
    for submission in subreddit_info.get_new(limit=1):
        post_dict[strip_title(submission.title)] = submission.url
        post_ids.append(submission.id)
    print "[STATUS] Generating short link using goo.gl"
    mini_post_dict = {}
    for post in post_dict:
        post_title = post
        post_link = post_dict[post]
        short_link = shorten(post_link)
        mini_post_dict[post_title] = short_link
    return mini_post_dict, post_ids

def setup_connection_reddit(subreddit):
    time = datetime.datetime.now().time()
    print str(time) + "\n[STATUS] setting up connection with Reddit"
    r = praw.Reddit('reddit melbourne twitter STATUS '
                    'monitoring %s' % (subreddit))
    subreddit = r.get_subreddit(subreddit)
    return subreddit

def shorten(url):
    # headers = {'content-type': 'application/json'}
    # payload = {"longUrl": url}
    # url = "https://www.googleapis.com/urlshortener/v1/url"
    # r = requests.post(url, data=json.dumps(payload), headers=headers)
    # link = json.loads(r.text)['id']
    return url

def duplicate_check(id):
    found = 0
    with open('posted_posts.txt', 'r') as file:
        for line in file:
            if id in line:
                found = 1
    return found

def add_id_to_file(id):
    with open('posted_posts.txt', 'a') as file:
        file.write(str(id) + "\n")

def main():
    logging.info('[STATUS] Script beginning')
    restart = True
    while restart == True:
        try:
            while True:
                restart = False
                subreddit = setup_connection_reddit('melbourne')
                post_dict, post_ids = tweet_creator(subreddit)
                tweeter(post_dict, post_ids)
        except Exception, e:
            restart = True
            print e
            print "[STATUS] Exception caught - sleeping 900 secs"
            time.sleep(900)

def tweeter(post_dict, post_ids):
    f = open('MelbourneReddit.txt')
    lines = f.readlines()
    f.close()
    access_token = lines[0].strip()
    access_token_secret = lines[1].strip()
    consumer_key = lines[2].strip()
    consumer_secret = lines[3].strip()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    for post, post_id in zip(post_dict, post_ids):
        found = duplicate_check(post)
        if found == 0:
            print "[STATUS] Posting this link on twitter"
            print post.encode('ascii', 'ignore') + " " + post_dict[post] + " #Melbourne"
            api.update_status(post.encode('ascii', 'ignore') + " " + post_dict[post] + " #Melbourne")

            print "[STATUS] Adding to file"
            add_id_to_file(post.encode('ascii', 'ignore'))
            print "[STATUS] Sleeping for 30 secs"
            time.sleep(30)
        else:
            print "[STATUS] Already posted"
            print "[STATUS] Sleeping for 30 secs"
            time.sleep(30)

main()
