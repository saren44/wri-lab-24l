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
hand = MediumMotor(OUTPUT_C)

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


class LineFollower:



    def __init__(self, checks, speed, hand_speed):
        self.followed_color = None
        self.is_black_followed = True
        self.turndir = None
        self.left_color = WHITE
        self.right_color = WHITE
        self.left_candidate = None
        self.right_candidate = None
        self.left_count = 0
        self.right_count = 0
        self.checks = checks
        self.speed = speed
        self.hand_speed = hand_speed
        self.state = 0
        pass

    def main_loop(self):
        self.check_colors()
        self.update_state()
        #print(self.state)
        if (self.state == 0):
            self.follow()
        elif (self.state == 1 or self.state == 2):
            self.color_turn()
        elif (self.state == 3):
            self.follow([BLACK, self.followed_color])
        elif self.state == 4:
            self.grab_object()
        elif self.state == 5:
            self.follow([BLACK, self.followed_color])
        elif self.state == 6 or self.state == 7:
            self.color_turn()
        elif self.state == 8:
            self.follow()
        elif self.state == 9 or self.state == 10:
            self.color_turn()
        elif self.state == 11:
            self.follow([BLACK, self.followed_color])
        elif self.state == 12:
            self.release_object()
        elif self.state == 13:
            self.follow([BLACK, self.followed_color])
        elif self.state == 14 or self.state == 15 or self.state == 16:
            self.color_turn()
        
        
        



    def check_colors(self):
        left = cl.color
        right = cr.color
        if (left == self.left_color):
            pass
        elif (left == self.left_candidate):
            self.left_count += 1
        elif (left in COLORS):
            self.left_candidate = left
            self.left_count = 1

        if (right == self.right_color):
            pass
        elif (right == self.right_candidate):
            self.right_count += 1
        elif (right in COLORS):
            self.right_candidate = right
            self.right_count = 1


        if (self.left_count >= self.checks):
            self.left_color = self.left_candidate
            #print("LEFT CHANGE: ", self.left_color)
        if (self.right_count >= self.checks):
            self.right_color = self.right_candidate
            #print("RIGHT CHANGE: ", self.right_color)
        #print(left, self.left_color, self.left_candidate, self.left_count)
        
    def update_state(self):
        if self.state == 0:
            if (self.left_color in COLORFUL_COLORS):
                self.state = 1
                self.followed_color = self.left_color
            elif (self.right_color in COLORFUL_COLORS):
                self.state = 2
                self.followed_color = self.right_color
            elif (self.left_color == BLACK and self.right_color == BLACK):
                self.state = 16
                self.followed_color = BLACK
        elif self.state == 3:
            if (self.left_color == self.followed_color and self.right_color == self.followed_color):
                self.state = 4
        elif self.state == 5:
            if (self.left_color == BLACK and self.right_color == BLACK):
                self.followed_color = BLACK
                if (self.turndir == 'l'):
                    self.state = 6
                else:
                    self.state = 7
        elif self.state == 8:
            if (self.left_color in COLORFUL_COLORS):
                self.state = 9
                self.followed_color = self.left_color
            elif (self.right_color in COLORFUL_COLORS):
                self.state = 10
                self.followed_color = self.right_color
        elif self.state == 11:
            if (self.left_color == self.followed_color and self.right_color == self.followed_color):
                self.state = 12
        elif self.state == 13:
            if (self.left_color == BLACK and self.right_color == BLACK):
                self.followed_color = BLACK
                if (self.turndir == 'l'):
                    self.state = 14
                else:
                    self.state = 15



    def follow(self, followed=[BLACK]):
        if (self.left_color not in followed and self.right_color not in followed):
            tank_drive.on(SpeedPercent(self.speed), SpeedPercent(self.speed))
        elif (self.left_color in followed and self.right_color in followed):
            tank_drive.on(SpeedPercent(self.speed / 2), SpeedPercent(self.speed / 2))
        elif (self.left_color in followed and self.right_color not in followed):
            tank_drive.on(SpeedPercent(-self.speed), SpeedPercent(self.speed))
        elif (self.left_color not in followed and self.right_color in followed):
            tank_drive.on(SpeedPercent(self.speed), SpeedPercent(-self.speed))

    
    def color_turn(self):
        sign = 0
        if self.state == 1 or self.state == 6 or self.state == 9 or self.state == 14 or self.state == 16:
            print('Turning left', self.left_color)
            self.turndir = 'l'
            sign = -1
        elif self.state == 2 or self.state == 7 or self.state == 10 or self.state == 15:
            sign = 1
            self.turndir = 'r'
            print('Turning right', self.right_color)
        else:
            print('Bad color')

        tank_drive.on_for_rotations(SpeedPercent(self.speed), SpeedPercent(self.speed), 0.5)
        for _ in range(self.checks + 1):
            self.check_colors()
        while ((sign == 1 and self.left_color != self.followed_color) or (sign == -1 and self.right_color != self.followed_color)):
            self.check_colors()
            tank_drive.on(SpeedPercent(self.speed * sign), SpeedPercent(-self.speed * sign))
            #print(self.turndir, self.right_color, self.followed_color)
        if (self.state == 16):
            self.state = 0
        elif (self.state == 1 or self.state == 2):
            self.state = 3
        elif (self.state == 6 or self.state == 7):
            self.state = 8
        elif (self.state == 9 or self.state == 10):
            self.state = 11
        elif self.state == 14 or self.state == 15:
            self.state = 0
        

    def grab_object(self):
        print('grabbing object')
        tank_drive.on_for_rotations(SpeedPercent(self.speed), SpeedPercent(self.speed), 0.25)
        hand.on_for_rotations(SpeedPercent(-self.hand_speed), 0.25)
        print('rotating 180')
        self.rotate()
        self.state = 5

    def release_object(self):
        print('releasing object')
        tank_drive.on_for_rotations(SpeedPercent(self.speed), SpeedPercent(self.speed), 0.25)
        hand.on_for_rotations(SpeedPercent(self.hand_speed), 0.25)
        print('rotating 180')
        self.rotate()
        self.state = 13
    
    def rotate(self):
        while not(self.left_color == WHITE):
            self.check_colors()
            tank_drive.on(SpeedPercent(-self.speed), SpeedPercent(self.speed))
        while not(self.left_color == BLACK or self.left_color == self.followed_color):
            self.check_colors()
            tank_drive.on(SpeedPercent(-self.speed), SpeedPercent(self.speed))
        while not(self.left_color == WHITE and (self.right_color == BLACK or self.right_color == self.followed_color)):
            self.check_colors()
            tank_drive.on(SpeedPercent(-self.speed), SpeedPercent(self.speed))


roboto = LineFollower(3, 15, 5)
while (True):
    roboto.main_loop()
