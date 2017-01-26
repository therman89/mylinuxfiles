import serial
from time import sleep 
import urllib
import urllib2
#import requests
import re
from datetime import datetime

class MeasData():
	ReadKey = '0'
	ID = 0
	humidity = 0.0
	temp = 0.0
	amblight = 0
	UV = 0
	RSSI = 0
	Vbat = 0
MEAS_DATA_LINES = 10
NumberOfLines = 0
nodecnt = 2
Node = [MeasData() for i in  range(nodecnt)]
ser = serial.Serial('/dev/ttyACM0',115200)
#ser = serial.Serial('COM17',115200)
ser.timeout = 1 
Node[0].ReadKey = 'DW24J25W85FHJ6XD'
Node[1].ReadKey = 'M6UVE1VBFQGNHNDI'

nodeidx = 0
while(True):
	line = ser.readline()
	line = line.strip()
	try:
		if(line != ''):
			print line
			NumberOfLines = NumberOfLines + 1
			words = line.split(':')
			#print words[0].strip()
			mName = words[0]
			words[1] = words[1].strip()
			try:
				mData = int(words[1])
			except ValueError:
				mData = float(words[1])
			if("Node" in mName):
				#print "Node data type " + str(type(mData))
				if (mData > 0 and mData <= nodecnt):
					nodeidx = mData-1
					#print "Node " + str(mData)
			elif("Humidity" in mName):
				Node[nodeidx].humidity = mData
				#print "Humidity " + str(mData)
			elif("Temperature" in mName):
				Node[nodeidx].temp = mData 
				#print "Temperature " + str(mData)
			elif("Ambient" in mName):
				Node[nodeidx].amblight = mData 
				#print "Ambient " + str(mData)
			elif("UV" in mName):
				Node[nodeidx].UV = mData 
				#print "UV " + str(mData)
			elif("RSSI" in mName):
				Node[nodeidx].RSSI = mData 
				#print "RSSI " + str(mData)
			elif("Battery" in mName):
				Node[nodeidx].Vbat = mData 
				#print "Vbat " + str(mData)
		else:#line is empty
			NumberOfLines = 0
			#print "Serial read timed out"	
		if(NumberOfLines ==  MEAS_DATA_LINES):			
			params = urllib.urlencode({'key': Node[nodeidx].ReadKey, 
				'field1': Node[nodeidx].temp,
				'field2': Node[nodeidx].humidity,
				'field3': Node[nodeidx].amblight,
				'field4': Node[nodeidx].RSSI,
				'field5': Node[nodeidx].Vbat})
			ret = urllib.urlopen("https://api.thingspeak.com/update", 
				data=params)
	#		print ret
	except IndexError:
		with open("log.txt",'a') as log:
			log.write(str(datetime.now()) + " Index error. Last data was:\n")
			log.write(line + "\n")
	except Exception as e:
		with open("log.txt",'a') as log:
			log.write(str(datetime.now()) + " Unhandled exception.\n" + str(e) + "\nLast data was:\n")
			log.write(line + "\n")
		
ser.close()

