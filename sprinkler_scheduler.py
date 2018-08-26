# -*- coding: utf-8 -*-
from crontab import CronTab
import datetime
import urllib2
from BeautifulSoup import BeautifulSoup

location = 'Budapest XIX'
contenturl = "http://www.amsz.hu/ws/index.php?view=currdat&user=CAD&num=1"
city = ''
soup = ''
user=[]
max_retries = 100
while user == [] and location not in city and max_retries:
    max_retries -= 1
    soup = BeautifulSoup(urllib2.urlopen(contenturl).read(), convertEntities=BeautifulSoup.HTML_ENTITIES)
    user = soup('a', attrs={'href': '../profile.php?lookup=CAD'})
    #print city, max_retries
if max_retries != 0:
    #print "Found user: ", user[0].find(text=True)
    precip = float(soup.find("td", text=u'Mai csapadék: ').parent.parent.findNext('td').findNext('td').text[:-2])
    #print 'Mai csapadék: ', precip, 'mm'
    # print precip
    temperature = float(soup.find("td", text=u'Hőmérséklet:').parent.parent.findNext('td').findNext('td').text[:-2])
    #print 'Hőmérséklet: ', temperature, '°C'
precip = 0
cron  = CronTab(user=True)
if precip >= 4: # and (5 < datetime.datetime.now().hour < 7):
    print "Morning Off"
    for job in cron.find_comment("Morning On"):
      job.enable(False)
else:
    print "Morning on"
    for job in cron.find_comment("Morning On"):
      job.enable()
if precip >= 8: # and (17 < datetime.datetime.now().hour < 19):
    print "Eveing off"
    for job in cron.find_comment("Evening On"):
      job.enable(False)
	else:
    print "Evening on"
    for job in cron.find_comment("Evening On"):
      job.enable()
cron.write()
