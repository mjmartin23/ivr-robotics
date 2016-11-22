#!/usr/bin/env python
# TASK A
import robot
import sys
if __name__ == '__main__':
    r = robot.Robot()
    if len(sys.argv) > 4:
        r.follower.follow(K=map(float,sys.argv[1:]))
    r.go()

# 9,0,1
# 
