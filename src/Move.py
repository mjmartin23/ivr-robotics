	
from Odometry import *
import time
	def forward(rob,speed=25,time=500,loop = True):
		rob.lMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		rob.rMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		
		if loop:
			while(rob.lMotor.state and rob.rMotor.state):
				rob.updateOdometry('forward')
				time.sleep(0.1)

			# adjust rob.x,rob.y
	def foward_till(rob,speed = 25,dist = 300,loop = True):
		rob.lMotor.run_to_rel_pos(duty_cycle_sp=speed,position_sp=dist )
		rob.rMotor.run_to_rel_pos(duty_cycle_sp=speed,position_sp=dist )
		if loop:
			while(rob.lMotor.state and rob.rMotor.state):
				pass
			rob.updateOdometry('forward')

	def backward(rob,speed=25,time=500,loop = True):
		rob.lMotor.run_timed(duty_cycle_sp=-speed, time_sp=time)
		rob.rMotor.run_timed(duty_cycle_sp=-speed, time_sp=time)
		rob.updateSensors()
		if loop:
			# adjust rob.x,rob.y
			while(rob.lMotor.state and rob.rMotor.state):
				pass
			rob.updateOdometry('backward')


	def rotate_left(rob,speed=25,time=500,loop = True):
		rob.rMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		rob.updateSensors()
		# adjust rob.x and rob.y
		if loop:
			while(rob.lMotor.state):
				pass
			rob.updateOdometry('turning')

	def rotate_left_till(rob,speed = 25,dist = 300,loop = True):
		rob.lMotor.run_to_rel_pos(duty_cycle_sp=speed,position_sp=dist )
		if loop:
			while(rob.lMotor.state):
				pass
			rob.updateOdometry('turning')

	def rotate_right_till(rob,speed = 25,dist = 300,loop = True):
		rob.rMotor.run_to_rel_pos(duty_cycle_sp=speed,position_sp=dist )
		if loop:
			while(rob.rMotor.state):
				pass
			rob.updateOdometry('turning')

	def rotate_right(rob,speed=25,time=500,loop = True):
		rob.lMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		if loop:
			while(rob.lMotor.state and rob.rMotor.state):
				pass
			rob.updateOdometry('turning')

	def rotateClockwise(rob,speed=25,time=500,loop = True):
		rob.right(speed=speed,time=time)
		rob.left(speed=-speed,time=time)
		if loop:
			while(rob.lMotor.state and rob.rMotor.state):
				pass
			rob.updateOdometry('turning')


	def rotateCounterClockwise(rob,speed=25,time=500,loop = True):
		rob.left(speed=speed,time=time)
		rob.right(speed=-speed,time=time)
		if loop:
			while(rob.lMotor.state and rob.rMotor.state):
				pass
			rob.updateOdometry('turning')


	def rotateDegrees(rob,degrees,loop = True):
		# implement from lab 2B
		clicks = deg_to_clicks(degrees)
		rob.left_till(dist = clicks)
		if loop:
			while(rob.lMotor.state and rob.rMotor.state):
				pass
			rob.updateOdometry('forward')
	def stopWheels(rob, l=False,r=False,update=True):
		if l:
			rob.lMotor.stop(stop_action = 'brake')
		if r:
			rob.rMotor.stop(stop_action = 'brake')
		if update:
			rob.updateOdometry()

	def go_to_ca(rob,distance,angle):
		clicks = cm_to_clicks(distance)
		rob.rotateDegrees(angle)
		time.sleep(0.5)
		rob.forward_till(dist = clicks)
		time.sleep(0.5)
		rob.rotateDegrees(final_angle)

	def go_to(x,y,theta)
    	angle,clicks = euclid_to_ca(x,y,theta)
    	final_angle = theta-angle

		rob.rotateDegrees(angle)
		time.sleep(0.5)
		rob.forward_till(dist = clicks)
		time.sleep(0.5)
		rob.rotateDegrees(final_angle)


	def rotateServo(rob):

		if rob.servoDirection == 'left' and rob.servo.position < -60:
			rob.servoDirection = 'right'
		elif rob.servoDirection == 'right' and rob.servo.position > 60:
			rob.servoDirection = 'left'
		if rob.servoDirection == 'left':
			rob.servo.run_timed(time_sp=10000,duty_cycle_sp=-25)
		else:
			rob.servo.run_timed(time_sp=10000,duty_cycle_sp=25)

	