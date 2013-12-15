# -*- coding: utf-8 -*-

import android
import time

class sensorsTest:

	def __init__(self, cnt):
		self.d = android.Android()
		self.total=cnt
		self.cnt=cnt
		self.d.wakeLockAcquireDim()
		self.d.startSensingTimed(1, 50)
		self.f = file('result.txt', 'w')
		self.d.makeToast('Sensor Test Initiating....')

	def __del__(self):
		self.d.wakeLockRelease()
		self.d.stopSensing()
		self.f.close()
		self.d.makeToast('Sensor Test Finished....')


	def test(self):
		while self.cnt:
			gRes = self.d.sensorsReadOrientation().result
			print gRes
			self.f.write('test #{0}: {1}\n'.format (self.total - self.cnt, gRes))
			time.sleep(0.1) # measure interval
			self.cnt -= 1


t = sensorsTest(300);
t.test();
