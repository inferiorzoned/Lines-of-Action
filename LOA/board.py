import pygame as pg
from .constants import *
from .piece import *

class Board:
    def __init__(self):
        self.boardList2d = []
        self.blacks_left = self.whites_left = 12
        
    def draw_checkBoard(self, win):
        for r in range(ROWS):
            # (c1, c2) = (CHECK1, CHECK2) if r%2 == 0 else (CHECK2, CHECK1)
            if r%2 == 0: c1, c2 = CHECK1, CHECK2
            else: c1, c2 = CHECK2, CHECK1
            for c in range(COLS):
                if c%2 == 0:
                    pg.draw.rect(win, c1, (r*SQUARE_SIZE, c*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pg.draw.rect(win, c2, (r*SQUARE_SIZE, c*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    
    def addPiecesToBoard(self):
        for r in range(ROWS):
            self.boardList2d.append([])
            for c in range(COLS):
                if r == 0 or r == ROWS-1:
                    p = Piece(r, c, BLACK) if c != 0 and c != COLS-1 else -1
                else:
                    p = Piece(r, c, WHITE) if c == 0 or c == COLS-1 else -1
                self.boardList2d[r].append(p)
    
    def drawUI(self, win):
        self.draw_checkBoard(win)
        self.addPiecesToBoard()
        for r in range(ROWS):
            for c in range(COLS):
                p = self.boardList2d[r][c]
                if p != -1:
                    p.draw_piece(win)
                    
    def move(self, piece, r, c):
        self.board[piece.row][piece.col], self.board[r][c] = self.board[r][c], self.board[piece.row][piece.col]
        piece.update(r, c)

            