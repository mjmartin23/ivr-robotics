# File for the lab assignments

import time

class PID:
    """docstring for PID"""
    def __init__(self, Kp=1, Ki=1, Kd=1, goal=0, interval = 0.005):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.goal = goal
        self.lastError = goal
        self.windup = goal*3
        self.currentTime = time.time()
        self.lastTime = self.currentTime
        self.interval = interval
        self.output = 0

    def set(self,goal,Kp=None,Ki=None,Kd=None,interval = 0.005):
        self.goal = goal
        self.lastError = goal
        self.currentTime = time.time()
        self.lastTime = self.currentTime
        self.interval = interval
        self.Kp = Kp if Kp is not None else self.Kp
        self.Ki = Ki if Ki is not None else self.Ki
        self.Kd = Kd if Kd is not None else self.Kd

    def update(self,currentVal):
        '''returns number of units to move according to PID controller
        '''
        error = self.goal - currentVal
        self.currentTime = time.time()
        deltaTime = self.currentTime - self.lastTime
        deltaError = error - self.lastError

        if deltaTime >= self.interval:
            pValue = self.Kp * error

            iValue += error
            iValue = min(max(-self.windup),error,self.windup)
            iValue *= self.Ki

            dValue = self.Kd * deltaError

            self.lastTime = self.currentTime
    	    self.lastError = error
            self.output = pValue + iValue + dValue
