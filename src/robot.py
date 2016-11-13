# Matt Martin, Dylan Angus
# 7/11/16
# Robot class

import ev3dev.ev3 as ev3
import time
import linefollow as flw

class Robot():
	"""docstring for Robot"""
	def __init__(self):
		# physical parts of robot
		self.lMotor = ev3.LargeMotor('B')
		self.rMotor = ev3.LargeMotor('C')
		self.gyro = ev3.GyroSensor(ev3.INPUT_2)
		self.sonar = ev3.UltrasonicSensor(ev3.INPUT_1)
		self.servo = ev3.MediumMotor('A')
		self.color = ev3.ColorSensor(ev3.INPUT_4)
		if not (self.lMotor.connected and self.rMotor.connected and self.gyro.connected and
			self.sonar.connected and self.color.connected and self.servo.connected):
			raise Exception("something isn't connected...")

		# readings from environment/state of robot
		self.x = 0
		self.y = 0
		self.gyroReading = 0
		self.sonarReading = 0
		self.colorReading = 0
		self.servoDirection = 'left'
		self.servo.run_to_abs_position(position_sp=0)
		self.updateSensors()

		# following state
    	self.follower = flw.CircleFollower(self)

		self.state = "initialized"

	def forward(self,speed=25,time=500):
		self.lMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		self.rMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		self.updateSensors()
		# adjust self.x,self.y

	def backward(self,speed=25,time=500):
		self.lMotor.run_timed(duty_cycle_sp=-speed, time_sp=time)
		self.rMotor.run_timed(duty_cycle_sp=-speed, time_sp=time)
		self.updateSensors()
		# adjust self.x,self.y

	def left(self,speed=25,time=500):
		self.rMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		self.updateSensors()
		# adjust self.x,self.y

	def right(self,speed=25,time=500):
		self.lMotor.run_timed(duty_cycle_sp=speed, time_sp=time)
		self.updateSensors()
		# adjust self.x,self.y

	def rotateClockwise(self,speed=25,time=500):
		self.right(speed=speed,time=time)
		self.left(speed=-speed,time=time)

	def rotateCounterClockwise(self,speed=25,time=500):
		self.left(speed=speed,time=time)
		self.right(speed=-speed,time=time)

	def rotateDegrees(self,degrees):
		# implement from lab 2B
		pass

	def goDistance(self,distance):
		# implement from lab 2B
		pass

	def rotateServo(self):
		if self.servoDirection == 'left' and self.servo.position < -30:
			self.servoDirection = 'right'
		elif self.servoDirection == 'right' and self.servo.position > 30:
			self.servoDirection = 'left'
		if self.servoDirection == 'left':
			self.servo.run_to_rel_position(position_sp=-4,speed_sp=30)
		else:
			self.servo.run_to_rel_position(position_sp=4,speed_sp=30)

	def updateSensors(self):
		self.gyroReading = self.gyro.value()
		self.sonarReading = self.sonar.value()
		self.colorReading = self.color.value()

	def changeFollowerType(self,follow):
		# follow is a child of LineFollower
		self.follower = follow

	def go(self):
		self.follower.go()

	def speakState(self):
		ev3.Sound.speak(self.state)

	def speak(self,string):
		ev3.Sound.speak(string)

if __name__ == '__main__':
	r = Robot()
	r.go()
