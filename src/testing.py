#! /usr/bin/env python
# Matt Martin, Dylan Angus
# 7/11/16

#Part 1 Testing forward travel
from robot import *
percs = range(1,11)
percs = [5*p for p in percs]
times = range(1,11)
times = [1000*t for t in times]
results=''
rob = Robot()
forward_results = open('forward_results','w')
for time in times:
    for t,p in zip([time for i in times],percs):
        rob.lMotor.run_timed(duty_cycle_sp=p, time_sp=t)
        rob.rMotor.run_timed(duty_cycle_sp=p, time_sp=t)
        while(rob.lMotor.state != []):
            print('here')
        print('out')
        l = rob.lMotor.position
        r = rob.rMotor.position
        results = results +str(t)+', '+str(p)+', ' +str(l) +', ' + str(r) +'\n'

forward_results.write(results)
forward_results.close()

#Part 2 Testing rotation
rob = Robot()

dists = range(1,11)
dists = [100*d for d in dists]
rotation_results = open('rotation_results','w')
results = ''
for dist in dists:
    rob.left_till(dist = dist)

    while(rob.lMotor.state!=[]):
        print('here')
    l = rob.lMotor.position
    g = rob.gyro.value()

    results = results +str(l) + ', ' + str(g) +'\n'
rotation_results.write(results)
rotation_results.close()
