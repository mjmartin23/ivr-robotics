#! /usr/bin/env python
# Matt Martin, Dylan Angus
# 7/11/16

from robot import *
import time

def collectObstacePIDData():
    r = Robot()
    outs = []
    base = 25
    r.follower.pid.set(100,Kp=1.875*0.015,Ki=1.875*0,Kd=1.875*0,window=5)
    r.follower.updateOnLine()
    t=0
    while not r.follower.onLine or t < 50:
        t+=1
        r.odometry.updateOdometry('')
        son = min(r.sonarReading,500)
        r.follower.pid.update(son)
        out = r.follower.pid.output
        outs.append([out,son])
        out = max(min(out,30),-30)
        r.lMotor.run_timed(duty_cycle_sp=30+out,time_sp=50)
        r.rMotor.run_timed(duty_cycle_sp=30-out,time_sp=50)
        r.follower.updateOnLine()

    r.mover.stopWheels(r=True,l=True,update=False)
    f = open('/home/robot/ivr-robotics/data/pidObstacle.txt','w')
    f.write('pidOut,sonarReadingGoalIs125\n')
    for out in outs:
        f.write('%f,%d\n' % (out[0],out[1]))
    f.close()

def collectPIDData():
    r = Robot()
    outs = []
    base = 25
    r.follower.pid.set(0,Kp=6.5,Ki=0.825,Kd=3.0,window=500)
    count = 0
    for i in range(200):
        r.follower.updateOnLine()
        r.follower.checkEdge()
        r.follower.pid.update(r.follower.edge)
        out = r.follower.pid.output
        print 'raw',out
        outs.append(r.follower.pid.output)
        out = max(min(out,2*base),-2*base)
        # if r.follower.edge < -.5:
        #     count += 1
        # else:
        #     count = 0
        # if count > 25:
        #     break
        r.follower.robot.lMotor.run_timed(duty_cycle_sp=base+out,time_sp=100)
        r.follower.robot.rMotor.run_timed(duty_cycle_sp=base-out,time_sp=100)
    r.mover.stopWheels(r=True,l=True,update=False)
    f = open('/home/robot/ivr-robotics/data/pid6-5_0-825_3.txt','w')
    for out in outs:
        f.write('%d\n' % out)
    f.close()


def findMotorPositionToMillimeters():
    rob = Robot()
    dists = range(100,700,50)
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
    f = open("/home/robot/ivr-robotics/data/motorDistance.txt","w")
    f.write(results)
    f.close()

def findMotorTurningToDegrees():
    rob = Robot()
    dists = range(100,700,50)
    results = "commandedMotorClicks,actualMotorClicksL,actualMotorClicksR,angleTurned\n"
    for dist in dists:
        initialAngle = rob.gyro.value()
        initialLeftMotor = rob.lMotor.position
        initialRightMotor = rob.rMotor.position
        rob.lMotor.run_to_rel_pos(duty_cycle_sp=25,position_sp=dist)
        rob.rMotor.run_to_rel_pos(duty_cycle_sp=25,position_sp=-dist)
        while rob.lMotor.state and rob.rMotor.state:
            pass
        time.sleep(0.75)
        endLeftMotor = rob.lMotor.position
        endRightMotor = rob.rMotor.position
        endAngle = rob.gyro.value()
        results += str(dist) + "," + str(endLeftMotor-initialLeftMotor) + "," + str(endRightMotor-initialRightMotor) + "," + str(initialAngle-endAngle) + "\n"
    f = open("/home/robot/ivr-robotics/data/rotationDistance.txt","w")
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
    #collectPIDData()
    #collectObstacePIDData()
    pass
