# File for the lab assignments

import ev3dev.ev3 as ev3
import time
import linefollow as flw
import robot as rob

def findObject(robot):
    while True:
        robot.rotateServo()
        robot.updateSensors()
        if robot.sonarReading < 500:
            robot.speak('found object within fifty centimeters')
            faceObject(robot)

def faceObject(robot):
    goalAngle = robot.servo.position
    initialAngle = robot.gyroReading

    
    while robot.gyroReading < robot.servo.position:
        #need to rotate robot clockwise
        robot.rotateClockwise()
        robot.updateSensors()

    while robot.gyroReading > robot.servo.position:
        #need to rotate robot clockwise
        robot.rotateCounterClockwise()
        robot.updateSensors()

def main():
    robot = rob.Robot()
    findObject(robot)

if __name__ == '__main__':
    main()
