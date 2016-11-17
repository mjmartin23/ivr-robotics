# Matt Martin, Dylan Angus
# 7/11/16
# Odometry class

import math

class Odometry:
	def __init__(self,robot):
		self.robot = robot

	def euclid_to_ca(self,x,y):
		angle = math.arctan(x,y)
		clicks = math.sqrt(x^2,y^2)*300/15
		return clicks, angle

	def cm_to_clicks(self,cent):
		return (300/15)*cent

	def deg_to_clicks(self,deg):
		return r*deg/2*math.pi

	def updateSensors(self, l=False,r=False,g=True,s=True,c=True):
		if(g):
			self.robot.gyroReading = self.robot.gyro.value()
		if(s):
			self.robot.sonarReading = self.robot.sonar.value()
			self.robot.servoReading = self.robot.servo.value()
		if(c):
			self.robot.colorReading = self.robot.color.value()
		if(r):
			self.robot.rw_pos = self.robot.rMotor.position
		if(l):
			self.robot.lw_pos = self.robot.lMotor.position

	def updateOdometry(self,action):
		theta = self.robot.theta
		if action == 'turning':
			theta = self.robot.gyro.value()-self.robot.gyroReading
			radius = self.robot.lbw
			self.robot.x = radius*math.cos(theta) + self.robot.x
			self.robot.y = radius*math.sin(theta) + self.robot.y
		elif action == 'turning_on_spot':
			pass
		else:
			#Retrieving previous left and right motor positions and direction of Rob
			l = self.robot.rw_pos
			r = self.robot.rw_pos
			theta = self.robot.theta
			#Retrieving half distance between the two wheels. Needed for calculations below.
			radius = self.robot.lbw/2
			diff = l-r
			#Case when the left wheel went further than the right
			if diff>0:
				#dist is the distance the left and right wheel travelled together on a straight line
				dist = r
			else:
				dist = l
			
			#alpha is the current direction of Rob
			alpha =self.robot.gyroReading

			#Change in direction between before and after action was taken
			dtheta = alpha -theta

			#Adjusting sign of radius is necessary for calculations. See report for further details.
			if alpha < 0:
				radius = -radius
			#Calculatng change in x and y after Rob finishes straight line and begins to turn
			dx = radius - radius*math.cos(dtheta)
			dy = radius + math.sin(dtheta)
			#Updating Rob's current belief of position
			self.robot.x = self.robot.x + dist*math.cos(theta) + dx 
			self.robot.y = self.robot.y + dist*math.sin(theta) + dy
			self.robot.theta = theta

		self.updateSensors(l = True,r = True)