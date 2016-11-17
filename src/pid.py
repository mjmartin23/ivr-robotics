# File for the lab assignments

import time

class PID:
    """docstring for PID"""
    def __init__(self, Kp, Ki, Kd, goal=0, interval = 0.01):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.goal = goal
        self.lastError = goal
        self.currentTime = time.time()
        self.lastTime = self.currentTime
        self.interval = interval

    def set(self,goal,interval = 0.01):
        self.goal = goal
        self.lastError = goal
        self.currentTime = time.time()
        self.lastTime = self.currentTime
        self.interval = interval

    def update(self,currentVal):
        '''returns number of units to move according to PID controller
        '''
        error = self.goal - currentVal
        self.currentTime = time.time()
        deltaTime = self.currentTime - self.lastTime
        deltaError = error - self.lastError

        if deltaTime >= self.interval:
            pValue = self.Kp * error

            iValue = 0

            dValue = self.Kd * (deltaError/deltaTime)

            self.lastTime = self.currentTime
    	    self.lastError = error
	    print pValue,dValue
            self.output = pValue + iValue + dValue
