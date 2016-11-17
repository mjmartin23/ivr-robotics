# Matt Martin, Dylan Angus
# 7/11/16
# LineFollower parent class and child classes
from Move import *
from Odometry import *
class LineFollower():
	"""robot should be of type Robot"""
	def __init__(self,robot):
		self.robot = robot
		# True if robot on line False otherwise
		self.updateOnLine()

	def updateOnLine(self):
		self.onLine = self.robot.colorReading < 30

	def follow(self):
		# return True if there is more line to be followed
		# return False if we got to the end of the line
		#
		# follow just moves one "step" forward, it's caller
		# will put it in a while loop

		self.robot.updateSensors()
		self.updateOnLine()

		# assuming a curve that is curving to the left,
		# turn forward when self.onLine = True,
		# turn left when self.onLine = False
		i = 0
		maxTurn = 500
		if self.onLine:
			while self.onLine:
				self.robot.rotate_right(time=50)
				self.updateOnLine()
		else:
			while not self.onLine and i < maxTurn:
				self.robot.rotate_left(time=50)
				self.updateOnLine()
				i += 1

		return i < maxTurn or self.onLine


		# OR

		# go forward when self.onLine = True,
		# figure out whether the line is to the left or
		#	to the right when self.onLine = False,
		# go that way

		# if self.onLine:
		# 	self.robot.forward()
		# else:
		# 	for i in range(4):
		# 		if i % 2 == 0:
		# 			self.robot.left(time=(i+1)*100)
		# 		else:
		# 			self.robot.right(time=(i+1)*100)
		# 		self.upateOnLine()
		# 		if self.onLine:
		# 			break

		# return self.onLine


	def go(self):
		# implement in child classes
		pass


class CircleFollower(LineFollower):
	"""docstring for CircleFollower"""
	def __init__(self, robot):
		LineFollower.__init__(self,robot)

	def go(self):
		# keep following the circle until some state is reached
		# (e.g. the program is quit? reaches end of line? unclear in assignment)

		while self.follow():
			pass
		self.robot.speak("reached end of line")


class BrokenLineFollower(LineFollower):
	"""docstring for CircleFollower"""
	def __init__(self, robot):
		LineFollower.__init__(self,robot)
		self.linesCompleted = 0

	def go(self):
		# continue untill we've finished all 4 lines
		while self.linesCompleted < 4:
			# follow() until reach end of line
			while self.follow():
				pass
			# increment self.linesCompleted
			self.linesCompleted += 1
			# speak end of line
			self.robot.speak("reached end of line %d" % (self.linesCompleted))

			self.findNextLine()

			self.robot.speak("found next line")

	def findNextLine(self):
		# find next line
		# line will be to the right if
		# self.linesCompleted % 2 == 1
		# it'll be on the left otherwise
		if self.linesCompleted % 2 == 0:
			# turn right until we've turned 90 degrees
			self.robot.updateSensors()
			self.robot.rotateDegrees(90+self.robot.gyroReading)

			# go forward until we find a line
			while not self.onLine:
				self.robot.forward()
				self.updateOnLine()

			# turn back to original heading

		else:
			# turn left until we've turned 90 degrees
			self.robot.updateSensors()
			self.robot.rotateDegrees(-90+self.robot.gyroReading)

			# go forward until we find a line
			while not self.onLine:
				self.robot.forward()
				self.updateOnLine()

			# turn back to original heading


class ObstacleAvoider(LineFollower):
	"""docstring for CircleFollower"""
	def __init__(self, robot):
		LineFollower.__init__(self,robot)
		self.obstacleFound = False

	def updateSonar():
		# 10 is arbitrary - we'll have to tune
		# self.robot.sonarDistance is in centimeters
		self.robot.rotateServo()
		self.obstacleFound = self.robot.sonarDistance < 100
		self.robot.updateSensors()
	def lookForObject(action=None):
		while not self.obstacleFound:
			if(action != None):
				action()
			self.updateSonar()
		self.robot.speak("Found object.")
		return self.robot.sonarDistance/10, self.robot.servoReading

	def go_to_Object():
		robot.forward(time = 50000,loop=False)
		dist,angle =lookForObject()
		self.robot.stopWheels(l =True,r=True)
		robot.go_to_ca(dist,angle)

	def go(self):
		# follow() until self.obstacleFound == True
		
		lookForObject(self.follow)
		self.robot.speak("Going to get around object.")
		# get closer to object using PI control (necessary?)
		# go around object
		# find line again
		# follow() to end of line
		# speak complete
