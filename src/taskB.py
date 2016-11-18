# TASK B
import robot
import linefollower as lfw
if __name__ == '__main__':
    r = robot.Robot()
    r.changeFollowerType(lfw.BrokenLineFollower())
    r.go()
