# Matt Martin, Dylan Angus
# 7/11/16
# Odometry class

import math

#Function calculating angle needed to rotate and hypothenusal distance to travel in wheel clicks from euclidean coordinates.
def euclid_to_ca(x, y):
  angle = math.arctan(x,y)
  clicks = math.sqrt(x^2,y^2)*300/15
return clicks, angle
def cm_to_clicks(cent):
	return (300/15)*cent
def deg_to_clicks(deg):
  return r*deg/2*math.pi
def updateSensors(rob, l=False,r=False,g=True,s=True,c=True):
	if(g):
		rob.gyroReading = rob.gyro.value()
	if(s):
		rob.sonarReading = rob.sonar.value()
		rob.servoReading = rob.servo.value()
	if(c):
		rob.colorReading = rob.color.value()
	if(r):
		rob.rw_pos = rob.rMotor.position
	if(l):
		rob.lw_pos = rob.lMotor.position
def updateOdometry(rob,action):
	theta = rob.theta
	if action == 'turning':
		theta = rob.gyro.value()-rob.gyroReading
		radius = rob.lbw
		rob.x = radius*math.cos(theta) + rob.x
		rob.y = radius*math.sin(theta) + rob.y
	elif action == 'turning_on_spot':
		pass
	else:
		#Retrieving previous left and right motor positions and direction of Rob
		l = rob.rw_pos
		r = rob.rw_pos
		theta = rob.theta
		#Retrieving half distance between the two wheels. Needed for calculations below.
		radius = rob.lbw/2
		diff = l-r
		#Case when the left wheel went further than the right
		if diff>0:
			#dist is the distance the left and right wheel travelled together on a straight line
			dist = r
		else:
			dist = l
		
		#alpha is the current direction of Rob
		alpha =rob.gyroReading

		#Change in direction between before and after action was taken
		dtheta = alpha -theta

		#Adjusting sign of radius is necessary for calculations. See report for further details.
		if alpha < 0:
			radius = -radius
		#Calculatng change in x and y after Rob finishes straight line and begins to turn
		dx = radius - radius*math.cos(dtheta)
		dy = radius + math.sin(dtheta)
		#Updating Rob's current belief of position
		rob.x = rob.x + dist*math.cos(theta) + dx 
		rob.y = rob.y + dist*math.sin(theta) + dy
		rob.theta = theta
	updateSensors(rob,l = True,r = True)
	