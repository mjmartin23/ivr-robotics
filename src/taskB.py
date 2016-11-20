#!/usr/bin/env python
# TASK B
import robot
import linefollow as lfw
if __name__ == '__main__':
    r = robot.Robot()
    r.changeFollowerType(lfw.BrokenLineFollower(r))
    r.go()
