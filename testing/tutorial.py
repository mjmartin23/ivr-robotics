# Some simple open loop scripts

import ev3dev.ev3 as ev3
import time
import utilities as util


def operateWheelsBasic():
    print "spin the wheels"

    Lmotor = ev3.LargeMotor('outB')
    Rmotor = ev3.LargeMotor('outC')
    Lmotor.connected
    Rmotor.connected

    # run_time takes milliseconds
    Lmotor.run_timed(duty_cycle_sp=25, time_sp=500)
    Rmotor.run_timed(duty_cycle_sp=25, time_sp=500)
    time.sleep(1)
    Lmotor.run_timed(duty_cycle_sp=-25, time_sp=500)
    Rmotor.run_timed(duty_cycle_sp=-25, time_sp=500)

    print('sleeping for 1 second')
    time.sleep(1)


def makeLightSwitch():
    print ("turn on LED w switch")
    print ("for 10 seconds")

    t_start = util.timestamp_now()
    ts = ev3.TouchSensor(ev3.INPUT_1)
    while True:
        ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[ts.value()])
        t_now = util.timestamp_now()
        if (t_now - t_start > 10E3):
            print ("finishing")
            break

    print ("turning off light")
    print (" ")
    ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[0])

def makeLightAndMotorSwitch():
    print ("drive forward and back")
    print ("using switches")
    print ("for 30 seconds")

    Lmotor = ev3.LargeMotor('outB')
    Rmotor = ev3.LargeMotor('outC')

    t_start = util.timestamp_now()
    ts = ev3.TouchSensor()
    ts2 = ev3.TouchSensor(ev3.INPUT_2)
    while True:
        ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[ts.value()])
        ev3.Leds.set_color(ev3.Leds.RIGHT, (ev3.Leds.GREEN, ev3.Leds.RED)[ts2.value()])

        if (ts.value()):
            Lmotor.run_timed(duty_cycle_sp=100, time_sp=50)
        elif (ts2.value()):
            Rmotor.run_timed(duty_cycle_sp=-100, time_sp=50)

        t_now = util.timestamp_now()
        if (t_now - t_start > 30E3):
            print ("im done")
            break

    print ("turning off light, done")
    ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[0])

def recordUltraSonic():
    print("Record readings from ultrasonic")
    print("Will print after back button is pressed")

    btn = ev3.Button()

    sonar = ev3.UltrasonicSensor(ev3.INPUT_1)
    sonar.connected
    sonar.mode = 'US-DIST-CM' # will return value in cm

    readings = ""
    readings_file = open('results.txt', 'w')

    while not btn.backspace:
        readings = readings + str(sonar.value()) + '\n'
    readings_file.write(readings)
    readings_file.close() # Will write to a text file in a column

def recordUltraSonicAndSonar():

    btn = ev3.Button()

    sonar = ev3.UltrasonicSensor(ev3.INPUT_1)
    sonar.connected
    sonar.mode = 'US-DIST-CM' # will return value in cm

    servo = ev3.MediumMotor('A')
    servo.run_to_abs_position(position_sp=0)
    i = 0
    while not btn.backspace:
        readings = readings + str(sonar.value()) + '\n'
        if sonar.value() < 1000:
            servo.run_to_rel_position(position_sp=i*30,duty_cycle_sp=30)
            i+=1
