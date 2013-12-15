# -*- coding: utf-8 -*-
'''
Description: Main algorithm to translate sensor readings into coordinates change
Author: Zheng Lu
Date: Dec.13, 2013
'''

import time

Pos, Neg = range(2)

SensingInterval = 10 # ms
SleepInterval = 0.02 # s

ShockResist = 0 # 0.1 / SleepInterval, not used in demo. Use it when you put the smartphone in pocket.
AThreshold = 1 # Threshold for step counting
StepSize = 0.7720000001 # meter, recommended by most pedometers

# these two values are for magnetometer readings, may need calibration. 
MShift = -65 # calibrate using min value of magnetometer readings
MMagnitude = 100 # calibrate using max - min value of magnetometer readings

RLatitude = 90000.0000000001 # how many meters for one degree of latitude, when Longitude = 36
RLongitude = 111000.0000000001 # how many meters for one degree of longitude

# in the following algorithm, we assume horizontally hold smartphone in hand
class SInterpreter:

	def __init__(self, d, f):
		self.d = d # android handler
		self.f = f # log file
		self.aAvg = 9.8 # recording the average of acceleration on x
		self.mAvg = 0.0 # recording the average of magnetic field on x

		self.d.wakeLockAcquireDim() # we have to keep screen on to get sensor readings, wakeLockPartial does not working, don't know why
		self.walkingState = Pos
		self.d.startSensingTimed(1, SensingInterval)

	def __del__(self):
		self.d.wakeLockRelease()
		self.d.stopSensing()
		self.d.vibrate(7000)

	# step count algorithm, also calculate average mag readings in each step
	def sensing(self):
		aAvg = self.aAvg # we can update this value on the run to make the algorithm more adaptive.
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

	# map sensor readings to coordinates and orientation change
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
