__author__ = 'graham'
import json
from urllib import urlopen

def main():
    url = urlopen('http://livetraffic.rta.nsw.gov.au/traffic/hazards/incident-open.json').read()
    data = json.loads(url)
    x = 0
    for i in data['features']:
        print data['features'][x]['properties']['headline']
        x += 1

if __name__ == '__main__':
    main()