#! /usr/bin/env python
# Matt Martin, Dylan Angus
# 7/11/16

#Part 1 Testing forward travel
from robot import *
import time

def forwards():
    percs = range(1,11)
    percs = [5*p + 20 for p in percs]
    times = range(1,6)
    times = [1000*t for t in times]
    results=''
    rob = Robot()

    for t in times:
        for p in percs:
            rob = Robot()
            rob.lMotor.run_timed(duty_cycle_sp=p, time_sp=t)
            rob.rMotor.run_timed(duty_cycle_sp=p, time_sp=t)
            while rob.lMotor.state and rob.rMotor.state:
                pass
            l = rob.lMotor.position
            r = rob.rMotor.position
            results += str(t)+', '+str(p)+', ' +str(l) +', ' + str(r) +'\n'
            rob.lMotor.run_timed(duty_cycle_sp=-p, time_sp=t)
            rob.rMotor.run_timed(duty_cycle_sp=-p, time_sp=t)
            while rob.lMotor.state and rob.rMotor.state:
                pass
    forward_results = open('forward_results.txt','w')
    forward_results.write(results)
    forward_results.close()

def turning():
    #Part 2 Testing rotation

    dists = range(1,1000,100)
    times = range(50,5000,50)
    rotation_results = open('rotation_results1.txt','w')
    results = ''
    #for dist in dists:
    for t in times:
        rob = Robot()
        g0 = rob.gyro.value()
        #rob.lMotor.run_to_rel_pos(duty_cycle_sp=25,position_sp=dist)
        #rob.rMotor.run_to_rel_pos(duty_cycle_sp=25,position_sp=-dist)
        rob.lMotor.run_timed(duty_cycle_sp=25,time_sp=t)
        rob.rMotor.run_timed(duty_cycle_sp=-25,time_sp=t)

        while rob.lMotor.state and rob.rMotor.state:
            pass
        time.sleep(1)
        l = rob.lMotor.position
        r = rob.rMotor.position
        g = rob.gyro.value() - g0

        results += str(t) + ', ' +str(l) + ', ' + str(r) + ', ' + str(g) +'\n'

    rotation_results.write(results)
    rotation_results.close()

if __name__ == '__main__':
    turning()
