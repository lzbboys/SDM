# -*- coding: utf-8 -*-
'''
Description: Main control logic, specialized for the demo
Author: Zheng Lu
Date: Dec.13, 2013
'''
import android
import time
import sInterpreter

d = android.Android()
f = open('log.txt', 'w')
source = open('polyline.temp', 'r')
lines = list(source)
source.close()
si = sInterpreter.SInterpreter(d, f)

MThreshold = 10
oldMagX = 0

# Using GPS to get the initial location
d.startLocating(1000, 30)
while 1:
	time.sleep(0.1)
	locatingReading = d.readLocation().result
	if 'gps' in locatingReading:
		coordinates = [locatingReading['gps']['latitude'], locatingReading['gps']['longitude']]
		d.makeToast('gps ready!')
		orientation = 'east'
		break

cnt = 150 # preset total step for each test, only used in demo
while cnt:
	magX = si.sensing()

	if magX - oldMagX > 10 or magX - oldMagX < -10:
		# call GPS to calibrate, we don't do that in this demo
		coordinates, orientation = si.calcCoordinates(coordinates, orientation, magX)
	else:
		coordinates, orientation = si.calcCoordinates(coordinates, orientation, magX)

	print 'New orientation is: {0}'.format(orientation)
	lines.insert(20, '\tnew google.maps.LatLng({0},{1}),\n'.format(coordinates[0], coordinates[1]))		# generate the file in an online way
	output = open('polyline.html', 'w')
	for l in lines:
		output.write(l)
	output.close()
	oldMagX = magX
	cnt -= 1

f.close()
