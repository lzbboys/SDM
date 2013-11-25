# -*- coding: utf-8 -*-

import time

Pos, Neg = range(2)

SensingInterval = 10 # ms
SleepInterval = 0.02 # s
# InitialSleep = 1 # s

ShockResist = 0 # 0.1 / SleepInterval
AThreshold = 1
StepSize = 0.7720000001 # meter, recommended by most pedometers

MShift = -65
MMagnitude = 100

RLatitude = 90000.0000000001 # meter, when Longitude = 36
RLongitude = 111000.0000000001

class SInterpreter:

	def __init__(self, d, f):
		self.d = d
		self.f = f
		self.aAvg = 9.8 # recording the average of acceleration on x
		self.mAvg = 0.0 # recording the average of magnetic field on x

		self.d.wakeLockAcquireDim()
		self.walkingState = Pos
		self.d.startSensingTimed(1, SensingInterval)
		# time.sleep(InitialSleep)

	def __del__(self):
		self.d.wakeLockRelease()
		self.d.stopSensing()
		self.d.vibrate(7000)

	def sensing(self):
		aAvg = self.aAvg
		shockcnt = 0
		mAvg = self.mAvg
		mTotal = 0
		mCnt = 0
		running = 1

		while running:
			# suppose phone is putting horizon in hand
			aRes = self.d.sensorsReadAccelerometer()
			mRes = self.d.sensorsReadMagnetometer()
			aX = aRes.result[2] if aRes.result[2] else aAvg
			mX = mRes.result[0] if mRes.result[0] else mAvg
			if not (aRes.result[0]) or not (mRes.result[0]):
				self.f.write('Invalid readings\n')
			if self.walkingState == Pos:
				if aX < (aAvg - AThreshold) and shockcnt > ShockResist:
					shockcnt = 0
					self.walkingState = Neg
			elif self.walkingState == Neg:
				if aX > (aAvg + AThreshold) and shockcnt > ShockResist:
					shockcnt = 0
					self.walkingState = Pos
					if mCnt != 0:
						mAvg = mTotal / mCnt 
					running = 0

			time.sleep(SleepInterval)
			shockcnt += 1
			if mRes.result[0]:
				mTotal += mX
				mCnt += 1

		return mAvg

	def calcCoordinates(self, coordinates, orientation, magX):
		if magX < MShift + MMagnitude and magX > MShift + 0.80*MMagnitude:
			# going west, longitude minus step size 
			orientation = 'west'
			coordinates[1] = coordinates[1] - StepSize / RLatitude
		elif magX < MShift + 0.74*MMagnitude and magX > MShift + 0.54*MMagnitude:
			# going north, latitude plus step size 
			orientation = 'north'
			coordinates[0] = coordinates[0] + StepSize / RLongitude
		elif magX < MShift + 0.47*MMagnitude and magX > MShift + 0.27*MMagnitude:
			# going sorth, latitude minus step size 
			orientation = 'south'
			coordinates[0] = coordinates[0] - StepSize / RLongitude
		elif magX < MShift + 0.2*MMagnitude and magX > MShift:
			# going east, longitude plus step size 
			orientation = 'east'
			coordinates[1] = coordinates[1] + StepSize / RLatitude
		else:
			# follow the original direction
			coordinates = coordinates
		return coordinates, orientation
