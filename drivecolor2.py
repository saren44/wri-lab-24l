#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.sensor import INPUT_2, INPUT_3


cl = ColorSensor(INPUT_2)
cr = ColorSensor(INPUT_3)
cl.mode = cl.MODE_COL_COLOR
cr.mode = cr.MODE_COL_COLOR
cl.calibrate_white()
cr.calibrate_white()
BLACK = cl.COLOR_BLACK
CG = cl.COLOR_GREEN
CR = cl.COLOR_RED
CB = cl.COLOR_BLUE
CY = cl.COLOR_YELLOW

colors = [CG, CR, CY]

WHITE = cl.COLOR_WHITE
RBLACK = cr.COLOR_BLACK
currentColor = None

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
hand = MediumMotor(OUTPUT_C)

SPEED = 10
HAND_SPEED = -5
is_holding = False


def color_turn(dir, col):
    if dir == 'left':
        print('Turning left')
        sign = -1
    elif dir == 'right':
        sign = 1
        print('Turning right')
    else:
        raise Exception('unexpected direction')

    tank_drive.on_for_seconds(SpeedPercent(SPEED), SpeedPercent(SPEED), 1)
    #tank_drive.on_for_seconds(SpeedPercent(SPEED * sign), SpeedPercent(-SPEED * sign), 3.9)
    while ((sign == 1 and cl.color != col) or (sign == -1 and cr.color != col)):
        tank_drive.on(SpeedPercent(SPEED * sign), SpeedPercent(-SPEED * sign))
    currentColor = col
    follow_black_and_color(col)

def rotate():
    print('rotating 180')
    total = 0
    while (total < 5):
        tank_drive.on(SpeedPercent(-SPEED), SpeedPercent(SPEED))
        if (cr.color == BLACK):
            total += 1

def check_for_color():
    color_found = False
    iters = 0
    while (color_found == False or iters < 20):
        tank_drive.on_for_rotations(SpeedPercent(SPEED / 4), SpeedPercent(-SPEED / 4), 0.005)
        iters += 1
        if (cl.color == currentColor):
            color_found = True
    if not color_found:
        tank_drive.on_for_rotations(SpeedPercent(-SPEED / 4), SpeedPercent(SPEED / 4), 0.5)
    return color_found
    
    

def back_on_track():
    print('returning to track')
    while (cl.color == BLACK):
        tank_drive.on(SpeedPercent(SPEED / 2), SpeedPercent(SPEED / 2))
    while (cl.color != BLACK):
        tank_drive.on(SpeedPercent(SPEED / 2), SpeedPercent(-SPEED / 2))
    follow_black()

def grab_object():
    print('grabbing object')
    tank_drive.on_for_seconds(SpeedPercent(SPEED), SpeedPercent(SPEED), 0.5)
    hand.on_for_rotations(SpeedPercent(HAND_SPEED), 0.25)
    is_holding = True
    rotate()

def release_object():
    print('releasing object')
    tank_drive.on_for_seconds(SpeedPercent(SPEED), SpeedPercent(SPEED), 0.8)
    hand.on_for_rotations(SpeedPercent(-HAND_SPEED), 0.25)
    tank_drive.on_for_seconds(SpeedPercent(SPEED), SpeedPercent(SPEED), 0.3)
    is_holding = False
    rotate()




def follow_black_and_color(color):
    colors = [BLACK, color]
    print('black and color')
    while(True):
        if (cl.color not in colors and cr.color not in colors):
            tank_drive.on(SpeedPercent(SPEED), SpeedPercent(SPEED))
        elif (cl.color in colors and cr.color in colors):
            tank_drive.on(SpeedPercent(SPEED / 2), SpeedPercent(SPEED / 2))
            if (cl.color == color and cr.color == color):
                if (is_holding):
                    release_object()
                else:
                    grab_object()
            elif (cl.color == BLACK and cr.color == BLACK):
                back_on_track()
        elif (cl.color  in colors and cr.color not in colors):
            tank_drive.on(SpeedPercent(-SPEED), SpeedPercent(SPEED))
        elif (cl.color not in colors and cr.color in colors):
            tank_drive.on(SpeedPercent(SPEED), SpeedPercent(-SPEED))

def follow_black():
    print('black')
    while(True):
        if (cl.color != BLACK and cr.color != BLACK):
            tank_drive.on(SpeedPercent(SPEED), SpeedPercent(SPEED))
            if cl.color in colors:
                color_turn('left', cl.color)
            elif cr.color in colors:
                color_turn('right', cr.color)
        elif (cl.color == BLACK and cr.color == BLACK):
            tank_drive.on(SpeedPercent(SPEED / 2), SpeedPercent(SPEED / 2))
        elif (cl.color == BLACK and cr.color != BLACK):
            tank_drive.on(SpeedPercent(-SPEED), SpeedPercent(SPEED))
            if cr.color in colors:
                color_turn('right', cr.color)
        elif (cl.color != BLACK and cr.color ==  BLACK):
            tank_drive.on(SpeedPercent(SPEED), SpeedPercent(-SPEED))
            if cl.color in colors:
                color_turn('left', cl.color)

def follow_black_return():
    print('black return')
    while(True):
        if (cl.color != BLACK and cr.color != BLACK):
            tank_drive.on(SpeedPercent(SPEED), SpeedPercent(SPEED))
        elif (cl.color == BLACK and cr.color == BLACK):
            back_on_track()
        elif (cl.color == BLACK and cr.color != BLACK):
            tank_drive.on(SpeedPercent(-SPEED), SpeedPercent(SPEED))
        elif (cl.color != BLACK and cr.color ==  BLACK):
            tank_drive.on(SpeedPercent(SPEED), SpeedPercent(-SPEED))


follow_black()