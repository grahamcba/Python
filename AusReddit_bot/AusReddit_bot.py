import praw
import json
import requests
import tweepy
import time
import datetime

def strip_title(title):
    if len(title) < 105:
        return title
    else:
        return title[:102] + "..."

def tweet_creator(subreddit_info):
    post_dict = {}
    post_ids = []
    print "[bot] Getting posts from Reddit"
    for submission in subreddit_info.get_new(limit=1):
        post_dict[strip_title(submission.title)] = submission.url
        post_ids.append(submission.id)
    print "[bot] Generating short link using goo.gl"
    mini_post_dict = {}
    for post in post_dict:
        post_title = post
        post_link = post_dict[post]
        short_link = shorten(post_link)
        mini_post_dict[post_title] = short_link
    return mini_post_dict, post_ids

def setup_connection_reddit(subreddit):
    time = datetime.datetime.now().time()
    print str(time) + "\n[bot] setting up connection with Reddit"
    r = praw.Reddit('reddit australia twitter bot '
                    'monitoring %s' % (subreddit))
    subreddit = r.get_subreddit(subreddit)
    return subreddit

def shorten(url):
    headers = {'content-type': 'application/json'}
    payload = {"longUrl": url}
    url = "https://www.googleapis.com/urlshortener/v1/url"
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    link = json.loads(r.text)['id']
    return link

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
    restart = True
    while restart == True:
        try:
            while True:
                restart = False
                subreddit = setup_connection_reddit('Australia')
                post_dict, post_ids = tweet_creator(subreddit)
                tweeter(post_dict, post_ids)
        except Exception, e:
            restart = True
            print e
            print "[bot] Exception caught - sleeping 30 secs"
            time.sleep(30)

def tweeter(post_dict, post_ids):
    f = open('AusReddit.txt')
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
            print "[bot] Posting this link on twitter"
            print post.encode('ascii', 'ignore') + " " + post_dict[post] + " #Australia"
            api.update_status(post.encode('ascii', 'ignore') + " " + post_dict[post] + " #Australia")

            print "[bot] Adding to file"
            add_id_to_file(post.encode('ascii', 'ignore'))
            print "[bot] Sleeping for 30 secs"
            time.sleep(30)
        else:
            print "[bot] Already posted"
            print "[bot] Sleeping for 30 secs"
            time.sleep(30)

if __name__ == '__main__':
    main()
