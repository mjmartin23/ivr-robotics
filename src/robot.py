# Matt Martin, Dylan Angus
# 7/11/16
# Robot class

import ev3dev.ev3 as ev3
import time
import linefollow as flw
import math
import odometry
import move

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

		self.mover = move.Move(self)
		self.odometry = odometry.Odometry(self)

		# readings from environment/state of robot
		self.odometry.updateSensors(l=True,r=True)

		# robot's position in space
		self.x = 0
		self.y = 0
		self.theta = self.gyroReading
		
		self.servo.run_to_abs_pos(position_sp=0,duty_cycle_sp=25)

		self.init_pos_r = self.rMotor.position
		self.init_pos_l = self.lMotor.position

		self.rel_pos_r = self.rMotor.position
		self.rel_pos_l = self.lMotor.position

		# following state
		self.follower = flw.CircleFollower(self)

		#Length between Rob's wheels
		self.lbw = 100*math.pi/11

	
	def changeFollowerType(self,follow):
		# follow is a child of LineFollower
		self.follower = follow

	def go(self):
		self.follower.go()

	def speak(self,string):
		ev3.Sound.speak(string)

if __name__ == '__main__':
	r = Robot()
	r.changeFollowerType(flw.BrokenLineFollower(r))
	r.go()
