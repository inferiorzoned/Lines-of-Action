# import pygame as pg
from pygame import draw
from .constants import SQUARE_SIZE, WHITEID, BLACKID, BLACK, WHITE

class Piece:
    PADDING = 17
    OUTLINE = 1

    def __init__(self, row, col, color, id):
        self.row = row
        self.col = col
        self.color = color
        self.id = id
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
    
        
    def draw_piece(self, win):
        rad = SQUARE_SIZE//2 - self.PADDING
        if self.id == WHITEID:
            draw.circle(win, BLACK, (self.x, self.y), rad + self.OUTLINE)    
        else:
            draw.circle(win, WHITE, (self.x, self.y), rad + self.OUTLINE)
         
        draw.circle(win, self.color, (self.x, self.y), rad)

    def update(self, r, c):
        self.row = r
        self.col = c
        self.calc_pos()
        
    
    def __str__(self):
        return f"row is {self.row}, col is {self.col}, color is {self.color}"