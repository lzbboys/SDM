import android
import time

class sensorsTest:
	def __init__(self, cnt):
		self.d = android.Android()
		self.total=cnt
		self.cnt=cnt
		self.d.makeToast("Sensor Test Initiating....")
		self.mx = -100
		self.mn = 100

	def test(self):
		self.d.startSensingTimed(1, 50)
		while self.cnt:
			mRes = self.d.sensorsReadMagnetometer().result
			if mRes[0]:
				m = mRes[0]
			if m > self.mx:
				self.mx = m
			if m < self.mn:
				self.mn = m
			print mRes[0]
			time.sleep(0.1) # measure interval
			self.cnt -= 1
		self.d.stopSensing()

		print 'max: {0}'.format(self.mx)
		print 'min: {0}'.format(self.mn)
		self.d.makeToast("Sensor Test Finished....")



t = sensorsTest(100);
t.test();
