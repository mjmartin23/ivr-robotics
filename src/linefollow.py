# Matt Martin, Dylan Angus
# 7/11/16
# LineFollower parent class and child classes

import time
import pid
import math

class LineFollower():
	"""robot should be of type Robot"""
	def __init__(self,robot):
		self.robot = robot
		self.updateOnLine()
		self.pid = pid.PID()
		self.obstacleFound = False
		self.edge = -1

	def updateOnLine(self):
		self.robot.odometry.updateOdometry('')
		self.onLine = self.robot.colorReading < 30

	def updateSonar(self,rotate=True,dist=200):
		# dist is arbitrary - we'll have to tune
		# self.robot.sonarReading is in millimeters
		if rotate:
			self.robot.mover.rotateServo()
		self.robot.odometry.updateOdometry('')
		self.obstacleFound = self.robot.sonarReading < dist

	def checkEdge(self):
		val = min(max(self.robot.colorReading,10),50) - 30
		self.edge = -math.tanh(val/20.0)

	def follow(self,side="right",sonar=False,dist=200,maxCount=None,maxGyro=45,K=[6.5,0.825,3.0,500]):
		# 6.0,0.6,0.5
		# 8 2.5 25 7
		# 12 1 3 500
		# BEST fot TASK C 9.5,0.675,3,500


		base = 25
		self.pid.set(0,K[0],K[1],K[2],window=int(K[3]))
		done = False
		count = 0
		g = self.robot.gyroReading
		diffGyro = 0
		sonarObjs = 0
		while not done:
			self.updateOnLine()
			self.checkEdge()
			self.pid.update(self.edge)
			out = self.pid.output
			out = max(min(out,2*base),-2*base)

			if self.edge < -.5:
				count = count + 1
				diffGyro = g - self.robot.gyroReading
			else:
				g = self.robot.gyroReading
				count = 0
			print count, diffGyro
			if maxCount is not None:
				if count > maxCount and abs(diffGyro) > maxGyro:
					break
			if side == 'left':
				self.robot.lMotor.run_timed(duty_cycle_sp=base+out,time_sp=100)
				self.robot.rMotor.run_timed(duty_cycle_sp=base-out,time_sp=100)
			else:
				self.robot.lMotor.run_timed(duty_cycle_sp=base-out,time_sp=100)
				self.robot.rMotor.run_timed(duty_cycle_sp=base+out,time_sp=100)
			if sonar:
				self.updateSonar(rotate=False,dist=dist)
				if self.obstacleFound:
					sonarObjs += 1
				else:
					sonarObjs = 0
				if sonarObjs > 5:
					break
		self.robot.mover.stopWheels(r=True,l=True,update=False)

	def go(self):
		# implement in child classes
		pass


class CircleFollower(LineFollower):
	"""docstring for CircleFollower"""
	def __init__(self, robot):
		LineFollower.__init__(self,robot)

	def go(self):
		# keep following the circle until reaches end of line
		self.robot.speak("following curved line")
		self.follow(side='left',maxCount=25,maxGyro=35)
		self.robot.speak("done")
		print 'done'


class BrokenLineFollower(LineFollower):
	"""docstring for CircleFollower"""
	def __init__(self, robot):
		LineFollower.__init__(self,robot)
		self.linesCompleted = 0

	def go(self):
		# continue untill we've finished all 5 lines
		self.robot.speak("following broken lines")
		self.updateOnLine()
		side = "left"
		while self.linesCompleted < 5:
			# follow() until reach end of line
			self.robot.speak("following line %d" % (self.linesCompleted+1))
			self.follow(side,maxCount=10,maxGyro=0)

			# increment self.linesCompleted
			self.linesCompleted += 1
			# speak end of line
			self.robot.speak("reached end of line %d" % (self.linesCompleted))

			if self.linesCompleted == 5:
				break
			self.robot.speak("looking for next line")

			self.findNextLine()

			side = "right" if side == "left" else "left"
			time.sleep(0.5)

		self.robot.speak("done")
		print "done"

	def findNextLine(self):
		# find next line
		# line will be to the right if
		# self.linesCompleted % 2 == 1
		# it'll be on the left otherwise

		# turn until we've turned 60 degrees
		self.robot.odometry.updateOdometry('')
		if self.linesCompleted % 2 == 1:
			self.robot.mover.rotateDegrees(60)
		else:
			self.robot.mover.rotateDegrees(-60)


		# go forward until we find a line
		self.updateOnLine()
		while not self.onLine:
			self.robot.mover.forward_till(loop=False)
			self.updateOnLine()
			self.robot.odometry.updateOdometry('')
		self.robot.mover.stopWheels(r=True,l=True,update=False)
		self.robot.speak("found next line")
		while self.onLine:
			self.robot.mover.forward_till(loop=False)
			self.updateOnLine()
			self.robot.odometry.updateOdometry('')
		self.robot.mover.stopWheels(r=True,l=True,update=False)

		# rotate to get into position for line following
		while not self.onLine:
			if self.linesCompleted % 2 == 1:
				self.robot.mover.rotate_right_till(dist=10,loop=False)
			else:
				self.robot.mover.rotate_left_till(dist=10,loop=False)
			self.updateOnLine()
		self.robot.mover.stopWheels(r=True,l=True,update=False)


class ObstacleAvoider(LineFollower):
	"""docstring for CircleFollower"""
	def __init__(self, robot):
		LineFollower.__init__(self,robot)
		self.obstacleMinAngle=360
		self.obstacleMaxAngle=-10000000
		self.obstacleMinDist=10000
		self.obstacleMaxDist=-1

	def lookForObject(self,action=None):
		# unused
		while not self.obstacleFound:
			if(action != None):
				action()
			self.updateSonar()
			self.robot.odometry.updateOdometry('')
		self.robot.mover.stopServor()
		self.robot.speak("Found object.")
		self.robot.mover.stopWheels(l =True,r=True)
		t=0
		while t<30:
			time.sleep(0.1)
			self.analyseObject()
			print t, self.obstacleMinDist/10, self.obstacleMinAngle, self.obstacleMaxAngle
			t+= 1
		self.robot.mover.stopServor()
		dist = self.obstacleMinDist
		return int(dist/10.0), (self.obstacleMaxAngle + self.obstacleMinAngle)/2

	def compare(self,d1,d2,epsilon):
		# unused
		if d2 > d1 - epsilon:
			if d2<d1+ epsilon:
				return 0
			else:
				return 1
		else:
			return -1

	def analyseObject(self):
		# unused
		self.robot.mover.rotateServo()
		self.robot.odometry.updateOdometry('')
		angle = self.robot.servoReading
		dist = self.robot.sonarReading
		angle = angle % 360
		if angle > 180:
			angle = angle - 360
		i = self.compare(self.obstacleMinDist,dist,5)
		j = self.compare(self.obstacleMinAngle,angle,2)
		if i < 0 and j < 1:
			self.obstacleMinAngle = angle
			self.obstacleMinDist = dist

		i = self.compare(self.obstacleMinDist,dist,5)
		j = self.compare(self.obstacleMaxAngle,angle,2)
		#print angle
		if i <= 0 and j > -1:
			self.obstacleMaxAngle = angle
			self.obstacleMinDist = dist


	def goToObject(self,safe=100):
		# unused
		self.robot.mover.forward(time = 50000,loop=False)
		distance,angle = self.lookForObject()
		distance = max(distance-7.5,0)
		distance = self.robot.odometry.cm_to_clicks(distance)
		self.robot.mover.stopWheels(l =True,r=True)

		self.robot.odometry.updateSensors()
		self.robot.mover.go_to_ca(distance,angle,final_angle=80-self.robot.gyroReading)


	def goAroundObject(self):
		# turn robot so it is parallel with object
		# turn sonar to look at object
		# set PID goal as distance to object
		# break when we find the line
		self.robot.mover.rotateDegrees(100)
		self.robot.servo.run_to_abs_pos(position_sp=-90,duty_cycle_sp=25)
		while self.robot.servo.state or self.robot.lMotor.state or self.robot.rMotor.state:
			pass
		time.sleep(0.5)
		self.robot.odometry.updateOdometry('')

		# trying to use PID - cleaner solution:
		# just set the pid goal as the sonar reading.
		self.pid.set(100,Kp=1.875*0.015,Ki=0,Kd=-0.001)
		self.updateOnLine()
		t=0
		while not self.onLine or t < 50:
			t+=1
			self.robot.odometry.updateOdometry('')
			son = min(self.robot.sonarReading,500)
			self.pid.update(son)
			out = self.pid.output
			out = max(min(out,30),-30)
			self.robot.lMotor.run_timed(duty_cycle_sp=30+out,time_sp=50)
			self.robot.rMotor.run_timed(duty_cycle_sp=30-out,time_sp=50)
			self.updateOnLine()

		self.robot.mover.stopWheels(r=True,l=True,update=False)

	def go(self):

		# follow line until sonar finds something within 75 mm
		self.follow(side='left',sonar=True,dist=75,K=[9.5,0.675,3,500])

		self.robot.speak("found object")

		self.robot.speak("Going around object.")
		self.goAroundObject()

		# found the line again, orient the robot for line following again
		self.robot.speak("went around object, found line again.")
		self.updateOnLine()
		while self.onLine:
			self.robot.mover.forward(speed = 30)
			self.updateOnLine()
			self.robot.odometry.updateOdometry('')
		while not self.onLine:
			self.robot.mover.rotate_left_till(dist=10,loop=False)
			self.updateOnLine()
			self.robot.odometry.updateOdometry('')
		self.robot.mover.stopWheels(r=True,l=True,update=False)
		self.robot.servo.run_to_abs_pos(position_sp=0,duty_cycle_sp=25)

		self.follow(side='left',sonar=True,dist=75, K=[12.5,0.675,3,500])

		self.robot.speak("completed a lap")
		self.robot.speak("done")
