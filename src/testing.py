#! /usr/bin/env python
# Matt Martin, Dylan Angus
# 7/11/16

#Part 1 Testing forward travel
from robot import *
import time

def findMotorPositionToMillimeters():
    rob = Robot()
    dists = range(50,500,50)
    results = "commandedMotorClicks,actualMotorClicksL,actualMotorClicksR,mmTraveled\n"
    for dist in dists:
        initialDistance = rob.sonar.value()
        initialLeftMotor = rob.lMotor.position
        initialRightMotor = rob.rMotor.position
        rob.lMotor.run_to_rel_pos(position_sp=dist,duty_cycle_sp=25)
        rob.rMotor.run_to_rel_pos(position_sp=dist,duty_cycle_sp=25)
        while rob.lMotor.state and rob.rMotor.state:
            pass
        time.sleep(0.5)
        endLeftMotor = rob.lMotor.position
        endRightMotor = rob.rMotor.position
        endDistance = rob.sonar.value()
        results += str(dist) + "," + str(endLeftMotor-initialLeftMotor) + "," + str(endRightMotor-initialRightMotor) + "," + str(initialDistance-endDistance) + "\n"
        rob.lMotor.run_to_rel_pos(position_sp=-dist,duty_cycle_sp=25)
        rob.rMotor.run_to_rel_pos(position_sp=-dist,duty_cycle_sp=25)
        while rob.lMotor.state and rob.rMotor.state:
            pass
        time.sleep(0.5)
    f = open("motorDistance.txt","w")
    f.write(results)
    f.close()

def findMotorTurningToDegrees():
    rob = Robot()
    dists = range(50,500,50)
    results = "commandedMotorClicks,actualMotorClicksL,actualMotorClicksR,angleTurned\n"
    for dist in dists:
        initialAngle = rob.gyro.value()
        initialLeftMotor = rob.lMotor.position
        initialRightMotor = rob.rMotor.position
        rob.lMotor.run_to_rel_pos(duty_cycle_sp=25,position_sp=dist)
        rob.rMotor.run_to_rel_pos(duty_cycle_sp=25,position_sp=-dist)
        while rob.lMotor.state and rob.rMotor.state:
            pass
        time.sleep(0.5)
        endLeftMotor = rob.lMotor.position
        endRightMotor = rob.rMotor.position
        endAngle = rob.gyro.value()
        results += str(dist) + "," + str(endLeftMotor-initialLeftMotor) + "," + str(endRightMotor-initialRightMotor) + "," + str(initialAngle-endAngle) + "\n"
        rob.lMotor.run_to_rel_pos(position_sp=-dist,duty_cycle_sp=25)
        rob.rMotor.run_to_rel_pos(position_sp=-dist,duty_cycle_sp=25)
        while rob.lMotor.state and rob.rMotor.state:
            pass
        time.sleep(0.5)
    f = open("rotationDistance.txt","w")
    f.write(results)
    f.close()

def forwards():
    percs = range(25,55,5)
    times = range(1000,6000,1000)
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
    #findMotorPositionToMillimeters()
    #findMotorTurningToDegrees()
    #forwards()
    #turning()
