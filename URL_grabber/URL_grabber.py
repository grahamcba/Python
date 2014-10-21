__author__ = 'graham'
__author__ = 'graham'
from bs4 import BeautifulSoup
import urllib2

big_url_list = []
def main():

    while len(big_url_list) < 1000:
        if len(big_url_list) == 0:
            url_worker()
        else:
            for i in big_url_list:
                print "Big URL list is: " + calculator()
                big_url_list.append("Next URL searched=" + i)
                url_worker(i)
                if len(big_url_list) > 5000:
                    break

def url_worker(wiki = None):

    if wiki == None:
        wiki = first_page()
    href_lister = href_loop(wiki)
    url_list = string_to_url(href_lister)

    f = open('big_url_list.txt', 'wb')
    for i in url_list:
        print i
        big_url_list.append(i)
        f.write(i + "\n")
    f.close()

def calculator():
    return str(len(big_url_list))

def href_loop(url):

    wiki = urllib2.urlopen(url).read()
    bs = BeautifulSoup(wiki)

    href_list = []
    for para in bs.find_all('p'):
        for link in para.find_all('a'):
            if "#" not in str(link):
                href_list.append(link.get('href'))

    return href_list[1:len(href_list)]

def first_page():
    catagory = raw_input("Enter /wiki/ catagory: ")
    url = 'http://en.wikipedia.org/wiki/' + catagory
    return url

def string_to_url(string):
    url_list= []
    for i in string:
        url = "http://en.wikipedia.org" + i
        url_list.append(url)
    return url_list



if __name__ == '__main__':
    main()