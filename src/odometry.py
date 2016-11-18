# Matt Martin, Dylan Angus
# 7/11/16
# Odometry class

import math

class Odometry:
	def __init__(self,robot):
		self.robot = robot

	def euclid_to_ca(self,x,y):
		angle = math.atan2(y,x)*180.0/math.pi
		cm = math.sqrt(x^2+y^2)
		clicks = self.cm_to_clicks(cm)
		return clicks, angle

	def cm_to_clicks(self,cent):
		#return (300/15)*cent
		mm = 10.0*cent
		constant = 0.4807090465
		return int(float(mm)/constant)

	def clicks_to_cm(self,clicks):
		constant = 0.4807090465
		return clicks*constant

	def deg_to_clicks(self,deg):
		#return self.robot.lbw*deg/2*math.pi
		constant = 0.4695354523
		return int(float(deg)/constant)

	def updateSensors(self, l=False,r=False,g=True,s=True,c=True):
		if(g):
			self.robot.gyroReading = self.robot.gyro.value()
		if(s):
			self.robot.sonarReading = self.robot.sonar.value()
			self.robot.servoReading = self.robot.servo.position
		if(c):
			self.robot.colorReading = self.robot.color.value()
		if(r):
			self.robot.rw_pos = self.robot.rMotor.position
		if(l):
			self.robot.lw_pos = self.robot.lMotor.position
		robot.timeLastUpdated = time.time()
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
			#Retrieving half distance between the two wheels. Needed for calculations below.
			lbw = self.robot.lbw
			#Retrieving previous left and right motor positions and direction of Rob

			pastl = self.robot.rw_pos
			pastr = self.robot.rw_pos
			deltaL = self.robot.lMotor.position
			deltaR = self.robot.rMotor.position
			deltaTime = time.time() - self.robot.timeLastUpdated()
			deltaC = (deltaR+deltaL)/2
			sci = (deltaR-deltaL)/lbw
			#alpha is the current direction of Rob
			alpha =self.robot.gyroReading
			theta = math.pi/2 - self.robot.theta
			dtheta = -alpha
			#Change in direction between before and after action was taken
			dtheta = alpha -theta

			#Updating Rob's current belief of position
			self.robot.x = self.robot.x + deltaC*cos(theta)
			self.robot.y = self.robot.y + dist*math.sin(theta) + dy
			self.robot.theta = theta

		self.updateSensors(l = True,r = True)
