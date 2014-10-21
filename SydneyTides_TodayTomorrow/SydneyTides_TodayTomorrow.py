from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
from astral import Astral
from datetime import datetime, timedelta
import pytz
import tweepy
import time

def main():
    global willyweather
    global soup
    global day
    global date
    global today
    global time_list
    global height_list
    global tide_level

    restart = True
    while restart == True:
        try:
            while True:
                restart = False
                print "\n[bot] Getting data from willyweather.com: "
                willyweather = urlopen('http://tides.willyweather.com.au/nsw/sydney/fort-denison.html').read()
                soup = bs(willyweather)
                day = bs(str(soup.find_all(class_="day-title")).replace('[', '').replace(']', '').replace(',',
                                                                                                          '')).get_text().split()
                date = bs(str(soup.find_all(class_="date-title")).replace('[', '').replace(']', '').replace(',',
                                                                                                            '')).get_text().split()
                time_list = bs(str(soup.find_all(class_="tide-time")).replace('[', '').replace(']', '').replace(',',
                                                                                                                '')).get_text().split()
                height_list = bs(
                    str(soup.find_all(class_="tide-height")).replace('[', '').replace(']', '').replace(' m',
                                                                                                       '').replace(',',
                                                                                                                   '')).get_text().split()
                tide_level = bs(
                    str(soup.find_all(class_="tide-level")).replace('[', '').replace(']', '').replace(' m', '').replace(
                        ',', '')).get_text().split()
                print "[bot] Tweet day one..."
                tweet(dayone())
                print "[bot] Sleeping 10 secs"
                time.sleep(10)
                print "[bot] Tweet day two..."
                tweet(daytwo())
                #print "[bot] Sleeping 10 secs"
                #time.sleep(10)
                #print "[bot] Tweet sunrise/set..."
                #tweet(sunriseset())
                print "[bot] Done - sleeping 10 minutes"
                time.sleep(600)
        except Exception, e:
            restart = True
            print e
            print "[bot] Exception caught - sleeping 10 minutes"
            time.sleep(600)


def dayone():
    lowtide_text = (day[0]) + " " + (date[1]) + " " + (date[0]) + " #Sydney" + "\n" + tide_level[0] + " tide: " + time_list[
        0] + " (" + height_list[0] + "m)" + " and " + time_list[2] + " (" + height_list[2] + "m)\n"
    hightide_text = tide_level[1] + " tide: " + time_list[1] + " (" + height_list[1] + "m)"
    if len(time_list[3]) > 3:
        hightide_text = tide_level[1] + " tide: " + time_list[1] + " (" + height_list[1] + "m)" + " and " + time_list[
            3] + " (" + height_list[3] + "m)"
    today, tomorrow = sunriseset()
    return lowtide_text + hightide_text + today


def daytwo():
    lowtide_text = (day[1]) + " " + (date[3]) + " " + (date[4]) + " #Sydney" + "\n" + tide_level[4] + " tide: " + time_list[
        4] + " (" + height_list[6] + "m)" + " and " + time_list[6] + " (" + height_list[4] + "m)\n"
    hightide_text = tide_level[5] + " tide: " + time_list[5] + " (" + height_list[5] + "m)"
    if len(time_list[7]) > 3:
        hightide_text = tide_level[5] + " tide: " + time_list[5] + " (" + height_list[5] + "m)" + " and " + time_list[
            7] + " (" + height_list[7] + "m)"
    today, tomorrow = sunriseset()
    return lowtide_text + hightide_text + tomorrow


def tweet(post):
    f = open('SydneyTides.txt')
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


def sunriseset():
    syd = 'Australia/Melbourne'
    u = datetime.utcnow()
    u = u.replace(tzinfo=pytz.utc)
    today = datetime.astimezone(u, pytz.timezone(syd))
    tomorrow = today + timedelta(days=1)
    a = Astral()
    location = a['Sydney']
    todaysun = location.sun(local=True, date=today)
    today_sunrise = todaysun['sunrise']
    today_sunset = todaysun['sunset']
    today_sunrise_text = "\nSunrise: " + str(today_sunrise.time())
    today_sunset_text = "\nSunset: " + str(today_sunset.time())

    tomorrowsun = location.sun(local=True, date=tomorrow)
    tomorrow_sunrise = tomorrowsun['sunrise']
    tomorrow_sunset = tomorrowsun['sunset']
    tomorrow_sunrise_text = "\nSunrise: " + str(tomorrow_sunrise.time())
    tomorrow_sunset_text = "\nSunset: " + str(tomorrow_sunset.time())
    today = (today_sunrise_text + today_sunset_text)
    tomorrow = (tomorrow_sunrise_text + tomorrow_sunset_text)

    return today, tomorrow


if __name__ == '__main__':
    main()