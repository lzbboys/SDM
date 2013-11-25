# -*- coding: utf-8 -*-

import android
import time

d = android.Android()
d.wakeLockAcquireDim()
d.startLocating(1000, 30)
f = open('result.txt', 'w')

cnt = 100
while cnt:
	res = d.readLocation().result
	if 'gps' in res:
		latitude = res['gps']['latitude']
		longitude = res['gps']['longitude']
		print 'GPS: Lat: {0}, Long: {1}'.format(latitude, longitude)
		f.write('GPS: {0}'.format(res['gps']))
	elif 'network' in res:
		latitude = res['network']['latitude']
		longitude = res['network']['longitude']
		print 'NET: Lat: {0}, Long: {1}'.format(latitude, longitude)
		f.write('NET: Lat: {0}, Long: {1}'.format(latitude, longitude))
	else:
		print 'None result'

	cnt -= 1
	time.sleep(1)

d.stopLocating()
d.wakeLockRelease()
