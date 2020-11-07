import pygame as pg

FPS = 60

WIDTH = HEIGHT = 960
ROWS = COLS = 8
SQUARE_SIZE = WIDTH//COLS

AImode = True

#COLORS
CHECK1 = pg.Color("#07a93d")
CHECK2 = pg.Color("#c1fa05")
BLACK = pg.Color("#000000")
WHITE = pg.Color("#ffffff")
REDDIRECTION = pg.Color("#ff3838")
BLUELINE = pg.Color("#0000ff")

#ID
BLACKID = 101
WHITEID = 102

#DIRECTION
UPDOWN = 0
LEFTRIGHT = 2
BOTTOMLEFT = 4
BOTTOMRIGHT = 6

DIRECTIONS = [UPDOWN, LEFTRIGHT, BOTTOMLEFT, BOTTOMRIGHT]

DIRX = [-1,1,0,0,1,-1,1,-1]
DIRY = [0,0,-1,1,-1,1,1,-1]

def withinBoard(r, c):
    return r >= 0 and r < ROWS and c >= 0 and c < COLS

pieceSquaretable = []
if ROWS == 8:
    pieceSquaretable = [
        [-80, -25, -20, -20, -20, -20, -25, -80],
        [-25, 10, 10, 10, 10, 10, 10, -25],
        [-20, 10, 25, 25, 25, 25, 10, -20],
        [-20, 10, 25, 50, 50, 25, 10, -20],
        [-20, 10, 25, 50, 50, 25, 10, -20],
        [-20, 10, 25, 25, 25, 25, 10, -20],
        [-25, 10, 10, 10, 10, 10, 10, -25],
        [-80, -25, -20, -20, -20, -20, -25, -80]
    ]
elif ROWS == 6:
    pieceSquaretable =  [
        [-80,  -20, -20, -20, -20,  -80],
        [-25,  10, 10, 10, 10,  -25],
        [-20,  25, 50, 50, 25,  -20],
        [-20,  25, 50, 50, 25,  -20],
        [-25,  10, 10, 10, 10,  -25],
        [-80,  -20, -20, -20, -20, -80]
    ]