# -*- coding: utf-8 -*-

import android
import sInterpreter

d = android.Android()
f = open('log.txt', 'w')
d.makeToast('SDM Path Recorder Initializing')
si = sInterpreter.SInterpreter(d, f)

coordinates = [35.95775, -83.92466] # should call GPS to initialize
MThreshold = 10
oldMagX = 0

cnt = 50

while cnt:
	magX = si.sensing()
	#print('Magnet on x %d: %f' % (cnt, magX))
	#f.write('Magnet on x %d: %f\n' % (cnt, magX))

	if magX - oldMagX > 10 or magX - oldMagX < -10:
		# call GPS to recalc
		coordinates = si.calcCoordinates(coordinates, magX)
	else:
		coordinates = si.calcCoordinates(coordinates, magX)

	# draw coordinates on the map
	print 'New coordinates are: {0}'.format(coordinates)
	oldMagX = magX
	cnt -= 1

f.close()
