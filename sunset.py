from crontab import CronTab
import datetime

cron  = CronTab(user=True)

from astral import Astral
city_name = 'Budapest'
try:
	a = Astral()
	a.solar_depression = 'civil'
	city = a[city_name]
	sun = city.sun(date=datetime.date.today(), local=True)
	[hour, minute] = sun['sunset'].time().hour, sun['sunset'].time().minute
	jobs = cron.find_comment("Stairs light")
	for item in jobs:
		job = item
	job.setall(minute, hour, '*', '*', '*')
	cron.write()
except Exception as e:
	print e.message



