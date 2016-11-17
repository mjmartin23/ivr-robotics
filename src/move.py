# Matt Martin, Dylan Angus
# 17/11/16
# Move class

import time
import pid
import math

class Move:
	"""docstring for Move"""
	def __init__(self, robot):
		self.robot = robot
		self.controller = pid.PID(1,1,1)
		self.servoDirection = 'left'

	def forward(self,speed=25,time=500,loop = True):
		self.robot.lMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		self.robot.rMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		if loop:
			while(self.robot.lMotor.state and self.robot.rMotor.state):
				self.robot.odometry.updateOdometry('forward')
				time.sleep(0.1)

	def forward_till(self,speed = 25,dist = 300,loop = True):
		self.robot.lMotor.run_to_rel_pos(duty_cycle_sp=speed,position_sp=dist )
		self.robot.rMotor.run_to_rel_pos(duty_cycle_sp=speed,position_sp=dist )
		if loop:
			while(self.robot.lMotor.state and self.robot.rMotor.state):
				pass
			self.robot.odometry.updateOdometry('forward')

	def backward(self,speed=25,time=500,loop = True):
		self.robot.lMotor.run_timed(duty_cycle_sp=-speed, time_sp=time)
		self.robot.rMotor.run_timed(duty_cycle_sp=-speed, time_sp=time)
		self.robot.odometry.updateSensors()
		if loop:
			while(self.robot.lMotor.state and self.robot.rMotor.state):
				pass
			self.robot.odometry.updateOdometry('backward')

	def goDistance(self,centimeters):
		clicks = self.robot.odometry.cm_to_clicks(centimeters)
		self.forward_till(dist=clicks,loop=False)

	def rotate_left(self,speed=25,time=500,loop = True):
		self.robot.rMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		if loop:
			while(self.robot.lMotor.state):
				pass
			self.robot.odometry.updateOdometry('turning')

	def rotate_left_till(self,speed = 25,dist = 300,loop = True):
		self.robot.lMotor.run_to_rel_pos(duty_cycle_sp=speed,position_sp=dist )
		if loop:
			while(self.robot.lMotor.state):
				pass
			self.robot.odometry.updateOdometry('turning')

	def rotate_right_till(self,speed = 25,dist = 300,loop = True):
		self.robot.rMotor.run_to_rel_pos(duty_cycle_sp=speed,position_sp=dist )
		if loop:
			while(self.robot.rMotor.state):
				pass
			self.robot.odometry.updateOdometry('turning')

	def rotate_right(self,speed=25,time=500,loop = True):
		self.robot.lMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		if loop:
			while(self.robot.lMotor.state and self.robot.rMotor.state):
				pass
			self.robot.odometry.updateOdometry('turning')

	def rotateClockwise(self,dist,speed=25,loop = True):
		self.robot.lMotor.run_to_rel_pos(position_sp=dist,duty_cycle_sp=speed)
		self.robot.rMotor.run_to_rel_pos(position_sp=-dist,duty_cycle_sp=speed)
		if loop:
			while(self.robot.lMotor.state and self.robot.rMotor.state):
				pass
			self.robot.odometry.updateOdometry('turning')


	def rotateCounterClockwise(self,dist,speed=25,loop = True):
		self.robot.lMotor.run_to_rel_pos(position_sp=-dist,duty_cycle_sp=speed)
		self.robot.rMotor.run_to_rel_pos(position_sp=dist,duty_cycle_sp=speed)
		if loop:
			while(self.robot.lMotor.state and self.robot.rMotor.state):
				pass
			self.robot.odometry.updateOdometry('turning')

	def rotate(self,clicks):
		self.robot.lMotor.run_to_rel_pos(position_sp=clicks,duty_cycle_sp=speed)
		self.robot.rMotor.run_to_rel_pos(position_sp=-clicks,duty_cycle_sp=speed)

	def rotateDegrees(self,degrees,loop = True):
		# implement from lab 2B
		clicks = self.robot.odometry.deg_to_clicks(degrees)
		#self.robot.left_till(dist = clicks)
		self.rotate(clicks)
		if loop:
			while(self.robot.lMotor.state and self.robot.rMotor.state):
				pass
			self.robot.odometry.updateOdometry('forward')

	def stopWheels(self, l=False,r=False,update=True):
		if l:
			self.robot.lMotor.stop(stop_action = 'brake')
		if r:
			self.robot.rMotor.stop(stop_action = 'brake')
		if update:
			self.robot.odometry.updateOdometry()

	def go_to_ca(self,distance,angle,final_angle = None):
		controller.set(angle)
    	while controller.error > 2:
    		self.robot.odometry.updateSensors()
	        controller.update(robot.gyroReading)
	        robot.rotateDegrees(controller.output)
		time.sleep(0.5)

		controller.set(0)
		while controller.error > 2:
    		self.robot.odometry.updateSensors()
	        controller.update(robot.gyroReading)
	        robot.goDistance(controller.output)
	    time.sleep(0.5)

	    if final_angle is not None:
			controller.set(final_angle)
	    	while controller.error > 2:
	    		self.robot.odometry.updateSensors()
		        controller.update(robot.gyroReading)
		        robot.rotateDegrees(controller.output)
			time.sleep(0.5)

	def go_to(self,x,y,theta)
    	angle = math.arctan(x,y)
    	distance = math.sqrt(x^2,y^2)
    	final_angle = theta-angle

    	self.go_to_ca(distance,angle,final_angle)

	def rotateServo(self):
		if self.servoDirection == 'left' and self.robot.servo.position < -60:
			self.servoDirection = 'right'
		elif self.servoDirection == 'right' and self.robot.servo.position > 60:
			self.servoDirection = 'left'
		if self.servoDirection == 'left':
			self.robot.servo.run_timed(time_sp=10000,duty_cycle_sp=-25)
		else:
			self.robot.servo.run_timed(time_sp=10000,duty_cycle_sp=25)

	