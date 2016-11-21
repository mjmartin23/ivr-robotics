# File for the lab assignments

import time

class PID:
    """docstring for PID"""
    def __init__(self, Kp=1, Ki=1, Kd=1, goal=0, interval = 0.005):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.pValue = 0
        self.iValue = 0
        self.dValue = 0
        self.goal = goal
        self.lastError = goal
        self.window = 7
        self.iQueue = []
        self.currentTime = time.time()
        self.lastTime = self.currentTime
        self.interval = interval
        self.output = 0

    def set(self,goal,Kp=None,Ki=None,Kd=None,interval = 0.005,window=7):
        self.pValue = 0
        self.iValue = 0
        self.dValue = 0
        self.goal = goal
        self.window = window
        self.lastError = goal
        self.currentTime = time.time()
        self.lastTime = self.currentTime
        self.interval = interval
        self.iQueue = []
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
            print 'e',error
            self.pValue = self.Kp * error

            self.iQueue.append(error)
            if len(self.iQueue) >= self.window:
                self.iQueue.pop(0)
            self.iValue = sum(self.iQueue) * self.Ki

            self.dValue = self.Kd * deltaError

            self.lastTime = self.currentTime
    	    self.lastError = error
            print self.pValue,self.iValue,self.dValue
            self.output = self.pValue + self.iValue + self.dValue
