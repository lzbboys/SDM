import android
import time

class sensorsTest:

	def __init__(self, cnt):
		self.d = android.Android()
		self.total=cnt
		self.cnt=cnt
		self.d.makeToast("Sensor Test Initiating....")

	def test(self):
		self.f = file('result.txt', 'a')

		self.d.startSensingTimed(1, 50)
		while self.cnt:
			
			aRes = self.d.sensorsReadAccelerometer().result 
			mRes = self.d.sensorsReadMagnetometer().result
			gRes = self.d.sensorsReadOrientation().result
			self.f.write('test #{0}: {1}{2}{3}\n' .format (self.total - self.cnt, aRes, mRes, gRes))
			time.sleep(0.1) # measure interval
			self.cnt -= 1
		self.d.stopSensing()

		self.f.close()
		self.d.makeToast("Sensor Test Finished....")



t = sensorsTest(200);
t.test();
