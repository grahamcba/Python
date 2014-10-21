import json
import urllib2
from bs4 import BeautifulSoup

def main():
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open('http://data.livetraffic.com/cameras/traffic-cam.json')
    code = BeautifulSoup(response)
    data = json.loads(str(code))
    x = 0
    for i in data['features']:
        url = data['features'][x]['properties']['href']
        print url
        filename = url.replace("http://www.rms.nsw.gov.au/trafficreports/cameras/camera_images/", "")
        print filename
        f = open(filename,'wb')
        f.write(urllib2.urlopen(url).read())
        f.close()
        x += 1

if __name__ == '__main__':
    main()