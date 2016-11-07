# Matt Martin, Dylan Angus
# 7/11/16
# LineFollower parent class

class LineFollower():
	"""docstring for LineFollower"""
	def __init__(self,robot):
		self.robot = robot
		# True if robot on line False otherwise
		self.state = True

	def updateState(self):
		self.state = self.robot.colorReading > 100