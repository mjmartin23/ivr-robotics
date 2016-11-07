# Matt Martin, Dylan Angus
# 7/11/16
# LineFollower parent class and child classes

class LineFollower():
	"""robot should be of type Robot"""
	def __init__(self,robot):
		self.robot = robot
		# True if robot on line False otherwise
		self.state = True

	def updateState(self):
		self.state = self.robot.colorReading > 40

	def follow(self):
		# follow line
		# turn right when self.state = True,
		# turn left when self.state = False

		# OR

		# go forward when self.state = True,
		# figure out whether the line is to the left or 
		#	to the right when self.state = False,
		# go that way

	def go(self):
		# implement in child classes
		pass


class CircleFollower(LineFollower):
	"""docstring for CircleFollower"""
	def __init__(self, robot):
		super(CircleFollower, self).__init__(robot)

	def go(self):
		pass
		
class BrokenLineFollower(LineFollower):
	"""docstring for CircleFollower"""
	def __init__(self, robot):
		super(BrokenLineFollower, self).__init__(robot)
		self.linesCompleted = 0

	def go(self):
		pass
		
class ObstacleAvoider(LineFollower):
	"""docstring for CircleFollower"""
	def __init__(self, robot):
		super(ObstacleAvoider, self).__init__(robot)
		self.obstacleFound = False

	def updateSonar():
		self.obstacleFound = self.robot.sonarDistance < 10

	def go(self):
		pass
