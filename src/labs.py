# File for the lab assignments

import robot as rob
import time

class PID:
    """docstring for PID"""
    def __init__(self, Kp, Ki, Kd, goal, interval = 0.01):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.goal = goal
        self.lastError = 0.0
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
            pValue = self.Kp * self.error

            iValue = 0

            dValue = self.Kd * (deltaError/deltaTime)

            self.lastTime = self.currentTime

            self.output = pValue + iValue + dValue


def findObject(robot):
    while True:
        robot.rotateServo()
        robot.updateSensors()
        if robot.sonarReading < 500:
            robot.speak('found object within fifty centimeters')
            break


def faceObject(robot):
    goalAngle = robot.servo.position
    initialAngle = robot.gyroReading
    controller = PID(robot,1,1,1,goalAngle)
    while controller.error > 5:
        controller.update(robot.gyroReading)
        robot.rotateDegrees(controller.output)


def goToObject(robot,safe):
    robot.updateSensors()
    distanceToTravel = robot.sonarReading-safe
    controller = PID(robot,1,1,1,distanceToTravel)
    while controller.error > 5:
        controller.update(robot.gyroReading)
        robot.goDistance(controller.output)

def main():
    robot = rob.Robot()
    findObject(robot)
    faceObject(robot)
    goToObject(robot,5)

if __name__ == '__main__':
    main()
