__author__ = 'graham'
import urllib2
from bs4 import BeautifulSoup

def main():

    url = urllib2.urlopen('http://www.sports-reference.com/cbb/boxscores/index.cgi?month=2&day=22&year=2014').read()
    bs = BeautifulSoup(url)
    table = bs.find_all(class_="no_highlight wide_table")

    OT_list = []
    x = 0
    for i in table:
        if "OT</td>" in str(i):
            if x % 2 == 0:
                OT_list.append(i)
        x += 1

    bs = BeautifulSoup(str(OT_list))
    teams = bs.find_all('a')

    teams_list = []
    for i in teams:
        if "2014.html" in str(i):
            teams_list.append(i.get_text())

    for i in range(0, len(teams_list), 2):
        print teams_list[i] + " vs " + teams_list[i+1]

if __name__ == '__main__':
    main()