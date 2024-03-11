#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.sensor import INPUT_2, INPUT_3


cl = ColorSensor(INPUT_2)
cr = ColorSensor(INPUT_3)
BLACK = cl.COLOR_BLACK
CG = cl.COLOR_GREEN
CR = cl.COLOR_RED
CB = cl.COLOR_BLUE
CY = cl.COLOR_YELLOW

colors = [CG, CR, CY, CB]
WHITE = cl.COLOR_WHITE
RBLACK = cr.COLOR_BLACK
currentColor = BLACK

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)


# drive in a different turn for 3 seconds


def left_color_turn(tank):
    print('left turn')
    tank_drive.on_for_seconds(SpeedPercent(10), SpeedPercent(10), 2)
    tank_drive.on_for_seconds(SpeedPercent(-10), SpeedPercent(10), 3.9)
    tank_drive.on_for_seconds(SpeedPercent(10), SpeedPercent(10), 5)
    currentColor = BLACK

def right_color_turn(tank):
    print('right turn')
    tank_drive.on_for_seconds(SpeedPercent(10), SpeedPercent(10), 2)
    tank_drive.on_for_seconds(SpeedPercent(10), SpeedPercent(-10), 3.9)
    tank_drive.on_for_seconds(SpeedPercent(10), SpeedPercent(10), 5)
    currentColor = BLACK

while(True):
    print(currentColor)
    if (currentColor != BLACK):
        if (cl.color != currentColor and cr.color != currentColor):
            tank_drive.on(SpeedPercent(10), SpeedPercent(10))
        elif (cl.color == currentColor and cr.color == currentColor):
            tank_drive.on(SpeedPercent(5), SpeedPercent(5))
        elif (cl.color != currentColor and cr.color == currentColor):
            right_color_turn(tank_drive)
        elif (cl.color == currentColor and cr.color != currentColor):
            left_color_turn(tank_drive)
    else:
        if (cl.color != currentColor and cr.color != currentColor):
            tank_drive.on(SpeedPercent(10), SpeedPercent(10))
            if cl.color in colors
                currentColor = cl.color
            elif cr.color in colors:
                currentColor = cr.color
        elif (cl.color == currentColor and cr.color == currentColor):
            tank_drive.on(SpeedPercent(5), SpeedPercent(5))
        elif (cl.color == currentColor and cr.color != currentColor):
            tank_drive.on(SpeedPercent(-10), SpeedPercent(10))
            if cr.color in colors:
                currentColor = cr.color
        elif (cl.color != currentColor and cr.color == currentColor):
            tank_drive.on(SpeedPercent(10), SpeedPercent(-10))
            if cl.color in colors:
                currentColor = cl.color
