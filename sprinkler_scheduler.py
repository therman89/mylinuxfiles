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
if max_retries != 0:
    precip = float(soup.find("td", text=u'Mai csapadék: ').parent.parent.findNext('td').findNext('td').text[:-2])
    print 'Mai csapadék: ', precip, 'mm'
    temperature = float(soup.find("td", text=u'Hőmérséklet:').parent.parent.findNext('td').findNext('td').text[:-2])
#    print 'Hőmérséklet: ', temperature, '°C'

cron  = CronTab(user=True)
if precip >= 4 and datetime.datetime.now().hour == 6:
    print "Morning Off"
    for job in cron.find_comment("Morning On"):
      job.enable(False)
else:
    print "Morning on"
    for job in cron.find_comment("Morning On"):
      job.enable()

morning_is_enabled = 0
for job in cron.find_comment("Morning On"):
      morning_is_enabled = job.is_enabled()
      if morning_is_enabled:
        print "Morning was enabled"
if (precip >= 8 or (precip >=4 and morning_is_enabled)) and datetime.datetime.now().hour == 18:
    print "Eveing off"
    for job in cron.find_comment("Evening On"):
      job.enable(False)
else:
    print "Evening on"
    for job in cron.find_comment("Evening On"):
      job.enable()
cron.write()
