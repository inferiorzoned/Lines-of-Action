import pygame as pg

FPS = 60

WIDTH = HEIGHT = 720

BUTTONHEIGHT = 160

class Dims:
    ROWS = COLS = None
    SQUARE_SIZE = None
    pieceSquaretable = None
    
    def generateDims(dim):
        Dims.ROWS = Dims.COLS = dim
        Dims.SQUARE_SIZE = WIDTH//dim    
        if dim == 8:
            Dims.pieceSquaretable = [
                [-80, -25, -20, -20, -20, -20, -25, -80],
                [-25, 10, 10, 10, 10, 10, 10, -25],
                [-20, 10, 25, 25, 25, 25, 10, -20],
                [-20, 10, 25, 50, 50, 25, 10, -20],
                [-20, 10, 25, 50, 50, 25, 10, -20],
                [-20, 10, 25, 25, 25, 25, 10, -20],
                [-25, 10, 10, 10, 10, 10, 10, -25],
                [-80, -25, -20, -20, -20, -20, -25, -80]
            ]
        elif dim == 6:
            Dims.pieceSquaretable =  [
                [-80,  -20, -20, -20, -20,  -80],
                [-25,  10, 10, 10, 10,  -25],
                [-20,  25, 50, 50, 25,  -20],
                [-20,  25, 50, 50, 25,  -20],
                [-25,  10, 10, 10, 10,  -25],
                [-80,  -20, -20, -20, -20, -80]
            ]

AImode = True

#COLORS
CHECK1 = pg.Color("#07a93d")
CHECK2 = pg.Color("#c1fa05")
BLACK = pg.Color("#000000")
WHITE = pg.Color("#ffffff")
REDDIRECTION = pg.Color("#ff3838")
BLUELINE = pg.Color("#0000ff")
WINBG = pg.Color("#fa7d7d")

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

DIR = [(-1,0), (1,0), (0,-1), (0,1), (1,-1), (-1,1), (1,1), (-1,-1)]

    
WINS = pg.transform.scale(pg.image.load('images/wins3.png'), (WIDTH//2, HEIGHT//3))
