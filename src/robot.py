# Matt Martin, Dylan Angus
# 7/11/16
# Robot class

import ev3dev.ev3 as ev3
import time
import utilities as util

class Robot():
	"""docstring for Robot"""
	def __init__(self):
		# physical parts of robot
		self.lMotor = ev3.LargeMotor('outB')
		self.rMotor = ev3.LargeMotor('outC')
		self.gyro = ev3.GyroSensor(ev3.INPUT_2)
		self.sonar = ev3.UltrasonicSensor(ev3.INPUT_4)
		self.color = ev3.ColorSensor(ev3.INPUT_3)
		self.lMmotor.connected
    	self.rMotor.connected
    	self.gyro.connected
    	self.sonar.connected
    	self.color.connected

    	# readings from environment/state of robot
		self.x = 0
		self.y = 0
		self.gyroAngle = 0
		self.sonarReading = 0
		self.colorReading = 0
		self.updateSensors()

		self.state = "initialized"

	def forward(self,speed=25,time=500):
		self.lMmotor.run_timed(duty_cycle_sp=speed, time_sp=time)
    	self.rMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
    	# adjust self.x,self.y

	def backward(self,speed=25,time=500):
		self.lMmotor.run_timed(duty_cycle_sp=-speed, time_sp=time)
    	self.rMotor.run_timed(duty_cycle_sp=-speed, time_sp=time)
    	# adjust self.x,self.y

	def left(self,speed=25,time=500):
		self.rMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		# adjust self.x,self.y

	def right(self,speed=25,time=500):
		self.lMmotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		# adjust self.x,self.y

	def updateSensors(self):
		self.gyroAngle = self.gyro.angle
		self.sonarDistance = self.sonal.distance_centimeters
		self.colorReading = self.color.reflected_light_intensity

	def go(self,follower):
		# follower is a child of LineFollower
		follower.go(self)

	def speakState(self):
		ev3.sound.speak(self.state)

if __name__ == '__main__':
	r = Robot()