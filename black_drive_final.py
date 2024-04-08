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
WHITE = cl.COLOR_WHITE

COLORS = [CG, CR, BLACK, WHITE]
COLORFUL_COLORS = [CG, CR]
BASE_COLORS = [BLACK, WHITE]


tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

#SPEED = 10
#HAND_SPEED = -5
is_holding = False

"""
STATES:
0 -> follow black
1 -> turning left
2 -> turning right
3 -> going after a color
4 -> grabbing
5 -> go on the line back to track
6 -> turn back left to track
7 -> turn back right to track
8 -> follow black with object
9 -> turn left to release the object
10 -> turn right to release the object
11 -> follow object release line
12 -> release object
13 -> turn back on track and set state to 0
16 -> helper to 90 turn
"""

statesDict = {
    0: lambda r, c: r.follow(),
    1: lambda r, c: r.color_turn(),
    2: lambda r, c: r.color_turn(),
    3: lambda r, c: r.follow([BLACK, c]),
    4: lambda r, c: r.grab_object(),
    5: lambda r, c: r.follow([BLACK, c]),
    6: lambda r, c: r.color_turn(),
    7: lambda r, c: r.color_turn(),
    8: lambda r, c: r.follow(),
    9: lambda r, c: r.color_turn(),
    10: lambda r, c: r.follow(),
    11: lambda r, c: r.color_turn([BLACK, c]),
    12: lambda r, c: r.release_object(),
    13: lambda r, c: r.color_turn([BLACK, c]),
    14: lambda r, c: r.color_turn(),
    15: lambda r, c: r.color_turn(),
    15: lambda r, c: r.color_turn(),
}

afterTurnDict = {
    1: 3,
    2: 3,
    6: 8,
    7: 8,
    9: 11,
    10: 11,
    14: 0,
    15: 0,
    16: 0
}

class LineFollower:



    def __init__(self, checks, speed, hand_speed):
        self.white_iters = 0
        self.left_color = WHITE
        self.right_color = WHITE
        pass

    def main_loop(self):
        self.check_colors()
        #self.update_state()
        #print(self.state)
        if (self.white_iters >= 100):
            self.line_check()
        self.follow()
        
        
        



    def check_colors(self):
        left = cl.color
        right = cr.color
        self.left_color = left
        self.right_color = right
        #print(left, self.left_color, self.left_candidate, self.left_count)

    
    def line_check(self):
        count = 0
        self.white_iters = 0
        while (self.left_color != BLACK and count < 75):
            self.check_colors()
            tank_drive.on(SpeedPercent(10), SpeedPercent(-10))
            count += 1
        if (self.left_color == BLACK):
            return
        while (self.left_color != BLACK and self.right_color != BLACK):
            self.check_colors()
            tank_drive.on(SpeedPercent(-30), SpeedPercent(-30))
        tank_drive.on_for_rotations(SpeedPercent(10), SpeedPercent(10), 0.5)
        self.check_colors()
        while (self.right_color != BLACK):
            self.check_colors()
            tank_drive.on(SpeedPercent(-10), SpeedPercent(10))
        



    def follow(self, followed=BLACK):

        if (self.left_color != BLACK and self.right_color != BLACK):
            self.white_iters += 1
            tank_drive.on(SpeedPercent(30), SpeedPercent(30))
        elif (self.left_color == BLACK and self.right_color == BLACK):
            self.white_iters = 0
            tank_drive.on(SpeedPercent(5), SpeedPercent(5))
            """
            if self.last_left:
                tank_drive.on(SpeedPercent(self.speed / 4), SpeedPercent(self.speed / 8))
                self.last_left = False
            else:
                tank_drive.on(SpeedPercent(self.speed / 8), SpeedPercent(self.speed / 4))
                self.last_left = True
            """
        elif (self.left_color == BLACK and self.right_color != BLACK):
            self.white_iters = 0
            tank_drive.on(SpeedPercent(-20), SpeedPercent(20))
        elif (self.left_color != BLACK and self.right_color == BLACK):
            self.white_iters = 0
            tank_drive.on(SpeedPercent(20), SpeedPercent(-20))

    


roboto = LineFollower(1, 30, 5)
while (True):
    roboto.main_loop()
