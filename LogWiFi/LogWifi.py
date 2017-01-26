import requests
import urllib2
import urllib
import time
import datetime
import re

form_url = "https://docs.google.com/forms/d/e/1FAIpQLScMp3diA0omf-ui6pzaSbSiU7aBVHhmN8hyW_j7sVXiWt9obw/formResponse"
params = urllib.urlencode({'key': 'RQQZ5DNA5C5UENIA', 'field1': '1'})


ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y.%m.%d. %H:%M:%S')
filepath = '/home/pi/LogWiFi/WifiTesterLog.log'

def check(url='http://www.google.com/', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
	submission = {"entry.332209985" : "True"}
	requests.post(form_url,submission)
	urllib.urlopen("https://api.thingspeak.com/update", data=params)
	
	file = open(filepath,'a')
	file.write(st+',1,'+get_external_ip()+'\n')
	file.close()
        return True
    except requests.ConnectionError:
	file = open(filepath,'a')
	file.write(st+',0\n')
	file.close()
        print("No internet connection available.")
    return False

def get_external_ip():
    site = urllib.urlopen("http://checkip.dyndns.org/").read()
    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
    address = grab[0]
    return address

check()
