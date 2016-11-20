# Matt Martin, Dylan Angus
# 7/11/16
# LineFollower parent class and child classes

import time
import pid

class LineFollower():
	"""robot should be of type Robot"""
	def __init__(self,robot):
		self.robot = robot
		# True if robot on line False otherwise
		self.updateOnLine()
		self.pid = pid.PID(1,1,1)
		self.obstacleFound = self.robot.sonarReading<400
	def updateOnLine(self):
		self.robot.odometry.updateSensors()
		if self.robot.colorReading < 15:
			self.onLine = 1
		elif self.robot.colorReading > 45:
			self.onLine = -1
		else:
			self.onLine = 0

	def updateSonar(self):
		# 10 is arbitrary - we'll have to tune
		# self.robot.sonarReading is in centimeters
		self.robot.mover.rotateServo()
		self.robot.odometry.updateSensors()
		self.obstacleFound = self.robot.sonarReading < 400

	def follow(self,side="right",sonar=False):
		# return True if there is more line to be followed
		# return False if we got to the end of the line
		#
		# follow just moves one "step" forward, it's caller
		# will put it in a while loop


		# assuming a curve that is curving to the left,
		# turn forward when self.onLine = True,
		# turn left when self.onLine = False
		# i = 0
		# maxTurn = 45
		# if self.onLine:
		# 	while self.onLine:
		# 		if side == "right":
		# 			self.robot.mover.rotate_right(speed=30,time=50,loop=False)
		# 		else:
		# 			self.robot.mover.rotate_left(speed=30,time=50,loop=False)
		# 		self.updateOnLine()
		# else:
		# 	while not self.onLine and i < maxTurn:
		# 		if side == "right":
		# 			self.robot.mover.rotate_left(speed=30,time=50,loop=False)
		# 		else:
		# 			self.robot.mover.rotate_right(speed=30,time=50,loop=False)
		# 		self.updateOnLine()
		# 		i += 1
		#
		# return i < maxTurn or self.onLine

		############
		#i = 0
		#while True:
		#	if self.onLine:
		#		self.robot.mover.forward(loop = False)
		#		self.robot.odometry.updateOdometry('')
		#		self.updateOnLine()
		#	direction =self.robot.angleVGyro>0
		#	if not self.onLine:
		#		if direction:
		#			self.robot.mover.rotate_left(speed=30,time=50,loop=False)
		#		else:
		#			self.robot.mover.rotate_right(speed=30,time=50,loop=False)
		#		self.updateOnLine()
		#		self.robot.odometry.updateOdometry('')
		#		i+=1
		#		if i>45:
		#			return True
		#	self.updateOnLine()

		self.pid.set(30,Ki=0.25,Kd=0.5)
		done = False
		count = 0
		while not done:
			self.robot.odometry.updateSensors()
			self.pid.update(self.robot.colorReading)
			out = self.pid.output
			# if out +30 > 100:
			# 	out = 70
			# elif out -30 <-100:
			# 	out = -70
			# shorter (maybe less readable though) below:
			out = max(min(out,70),-70)
			count = 0 if out > 0 else count + 1
			if count > 500:
				break
			if side == 'left':
				self.robot.lMotor.run_timed(duty_cycle_sp=30+out,time_sp=50)
				self.robot.rMotor.run_timed(duty_cycle_sp=30-out,time_sp=50)
			else:
				self.robot.lMotor.run_timed(duty_cycle_sp=30-out,time_sp=50)
				self.robot.rMotor.run_timed(duty_cycle_sp=30+out,time_sp=50)
			if sonar:
				self.updateSonar()
				if self.obstacleFound:
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
		# while self.follow():
		# 	pass
		self.follow()
		self.robot.speak("done")
		print 'done'


class BrokenLineFollower(LineFollower):
	"""docstring for CircleFollower"""
	def __init__(self, robot):
		LineFollower.__init__(self,robot)
		self.linesCompleted = 0

	def go(self):
		# continue untill we've finished all 4 lines
		self.robot.speak("following broken lines")
		self.updateOnLine()
		print self.onLine
		side = "right"
		while self.linesCompleted < 4:
			# follow() until reach end of line
			self.robot.speak("following line %d" % (self.linesCompleted+1))
			self.follow(side)

			# increment self.linesCompleted
			self.linesCompleted += 1
			# speak end of line
			self.robot.speak("reached end of line %d" % (self.linesCompleted))

			if self.linesCompleted == 4:
				break
			try:
				self.robot.speak("looking for next line")
			except Exception:
				pass
			self.findNextLine()
			try:
				self.robot.speak("found next line")
			except Exception:
				pass
			side = "right" if side == "left" else "left"
			time.sleep(1)

		self.robot.speak("done")

	def findNextLine(self):
		# find next line
		# line will be to the right if
		# self.linesCompleted % 2 == 1
		# it'll be on the left otherwise
		if self.linesCompleted % 2 == 1:
			# turn right until we've turned 70 degrees
			self.robot.odometry.updateSensors()
			self.robot.mover.rotateDegrees(45-self.robot.gyroReading)

			# go forward until we find a line
			while not self.onLine:
				self.robot.mover.forward(loop=False)
				self.updateOnLine()
				self.robot.odometry.updateOdometry('')
			self.robot.mover.stopWheels(r=True,l=True,update=False)
			# turn back to original heading
			while self.onLine:
				self.robot.mover.rotateCounterClockwise(self.robot.odometry.deg_to_clicks(50),loop=False)
				self.updateOnLine()
				self.robot.odometry.updateOdometry('')
			self.robot.mover.stopWheels(r=True,l=True,update=False)


		else:
			# turn left until we've turned 70 degrees
			self.robot.odometry.updateSensors()
			self.robot.mover.rotateDegrees(-45-self.robot.gyroReading)

			# go forward until we find a line
			while not self.onLine:
				self.robot.mover.forward(loop=False)
				self.updateOnLine()
				self.robot.odometry.updateOdometry('')
			self.robot.mover.stopWheels(r=True,l=True,update=False)

			# turn back to original heading
			while self.onLine:
				self.robot.mover.rotateClockwise(self.robot.odometry.deg_to_clicks(50),loop=False)
				self.updateOnLine()
				self.robot.odometry.updateOdometry('')
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
		#print self.obstacleMinDist/10.0, (self.obstacleMaxAngle + self.obstacleMinAngle)/2
		dist = round(self.obstacleMinDist/0.480709)
		return int(dist), (self.obstacleMaxAngle + self.obstacleMinAngle)/2
	def compare(self,d1,d2,epsilon):
		if d1 > d2 + epsilon:
			return -1
		elif d1<d2+ epsilon:
			return 0
		else:
			return 1
	def analyseObject(self):
				self.robot.mover.rotateServo()
				self.robot.odometry.updateSensors()
				angle = self.robot.servoReading
				dist = self.robot.sonarReading
				angle = angle % 360
				if angle >180:
					angle = 180-angle
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


	def goToObject(self,safe=10):
		self.robot.mover.forward(time = 50000,loop=False)
		distance,angle = self.lookForObject()
		self.robot.mover.stopWheels(l =True,r=True)
		#distance= self.robot.odometry.cm_to_clicks(distance)
		#print distance
		print distance
		self.robot.mover.go_to_ca(distance,angle)

		# get closer to object using PD control
		#dist,angle = self.robot.sonarReading/10, self.robot.servoReading
		# buffer of safe cm from object
		#self.robot.mover.go_to_ca(dist-safe,angle)
		#self.robot.servo.run_to_rel_pos(position_sp=0,duty_cycle_sp=25)

	def goAroundObject(self):
		# possible algorithm:
		# turn robot 90 degrees so it is parallel with object
		# turn sonar to look at object
		# drive forward until sonar doesnt see an object anymore
		# repeat until we find the line
		self.robot.mover.rotateDegrees(90)
		self.robot.servo.run_to_rel_pos(position_sp=-90,duty_cycle_sp=25)
		while (self.robot.lMotor.state and self.robot.rMotor.state and self.robot.servo.state):
			pass

		self.robot.odometry.updateSensors()
		# lastSonar = self.robot.sonarReading
		# while not self.onLine:
		# 	# go forward a small amount
		# 	# if object is no longer there
		# 	# 	go forward another small amount to be sure turning doesn't collide
		# 	#	turn left 90 degrees
		# 	#	go forward till we find the object again
		# 	if self.robot.sonarReading < 200:
		# 		# we're getting dangerously close to the object, turn right a little
		# 		self.robot.speak("got too close to object, turning right")
		# 		self.robot.mover.rotateClockwise(10)

		# 	self.robot.mover.forward_till(dist=100,loop=False)
		# 	self.robot.odometry.updateSensors()
		# 	if self.robot.sonarReading - lastSonar > 1000:
		# 		self.robot.mover.forward_till(dist=500)
		# 		self.robot.rotateDegrees(-90)
		# 		self.robot.odometry.updateSensors()
		# 		while self.robot.sonarReading > 500:
		# 			self.robot.mover.forward_till(dist=200,loop=False)
		# 			self.robot.odometry.updateSensors()
		# 		self.robot.mover.stopWheels(r=True,l=True)
		# 	lastSonar = self.robot.sonarReading
		# 	self.updateOnLine()


		#####

		# trying to use PID - cleaner solution:
		# just set the pid goal as the sonar reading.
		self.pid.set(self.robot.sonarReading,Kp=0.25,Kd=0.5)
		self.updateOnLine()
		while not self.onLine:
			self.robot.odometry.updateSensors()
			self.pid.update(self.robot.sonarReading)
			out = self.pid.output
			out = max(min(out,45),-45)
			self.robot.lMotor.run_timed(duty_cycle_sp=30-out,time_sp=50)
			self.robot.rMotor.run_timed(duty_cycle_sp=30+out,time_sp=50)
			self.updateOnLine()

		self.robot.mover.stopWheels(r=True,l=True,update=False)

	def go(self):

		#lookForObject(self.follow)
		self.follow(sonar=True)

		self.robot.speak("found object. getting closer to object.")
		self.goToObject()

		self.robot.speak("Going to get around object.")
		self.goAroundObject()

		self.robot.speak("went around object, found line again.")
		self.follow():

		self.robot.speak("reached end of line")
		self.robot.speak("done")
