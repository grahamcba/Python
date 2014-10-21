__author__ = 'Graham'
from bs4 import BeautifulSoup as bs
import urllib2
import pyimgur
import datetime
import tweepy
from PIL import Image
import requests
import json
import time as t

global time

def main():
    restart = True
    while restart == True:
        try:
            while True:
                restart = False
                time = datetime.datetime.now().time()
                print "[bot] " + str(time)
                print "[bot] Opening BOM site..."
                willyweather = urllib2.urlopen('http://www.bom.gov.au/products/IDR713.shtml#skip').read()
                soup = bs(willyweather)
                day = soup.find('img', alt="128 km Sydney (Terrey Hills) Radar")['src']
                print "[bot] Saving radar image..."
                f = open('Radar.jpg','wb')
                f.write(urllib2.urlopen('http://www.bom.gov.au'+day).read())
                f.close()
                Image.open('Radar.jpg').convert('RGB').save('Radar.jpg')
                f.close()
                imgur_url = imgur()
                tweet(imgur_url)
                print '[bot] -----Sleeping for 30 mins-----'
                t.sleep(1800)
        except Exception, e:
            restart = True
            print e
            print "[bot] Exception caught - sleeping 10 minutes"
            t.sleep(600)

def imgur():
    API_KEY = 'afd0e68ba523a4888719ad691ff4311d465c8420'
    CLIENT_ID = '11f0413f1ce0302'
    PATH = "Radar.jpg"
    print "[bot] Uploading to Imgur..."
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH)
    print "[bot] Uploaded"
    print "[bot] URL: " + (uploaded_image.link)
    url = uploaded_image.link[0:-4]
    return (url)

def shorten(url):
    headers = {'content-type': 'application/json'}
    payload = {"longUrl": url}
    url = "https://www.googleapis.com/urlshortener/v1/url"
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    link = json.loads(r.text)['id']
    return link

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
    post = t.strftime("%H:%M : ") + "128 km Sydney (Terrey Hills) Radar #Sydney " + post
    api.update_status(post.encode('ascii','ignore'))
    postsize = len(post)
    print "[bot] Posted: \n" + post.encode('ascii','ignore')
    print "[bot] Length: " + str(postsize)


if __name__ == '__main__':
    main()