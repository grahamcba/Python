__author__ = 'graham'
import requests
import json


def shorten(url):
    headers = {'content-type': 'application/json'}
    payload = {"longUrl": url}
    url = "https://www.googleapis.com/urlshortener/v1/url"
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    link = json.loads(r.text)['id']
    return link

if __name__ == '__main__':
    shorten("www.bbc.co.uk/news")