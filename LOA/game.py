# import pygame as pg
from pygame import display, draw
import sys
from .ai import *
from .constants import BLACKID, WHITEID, SQUARE_SIZE, REDDIRECTION, BLUELINE, AImode
from .board import Board

# import sys, os, inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)


class Game:
    def __init__(self, win):
        self.board = Board()
        self.selectedPiece = None
        self.turn = BLACKID
        self.op = WHITEID
        self.validMoves = set()
        self.win = win
        self.fromPos = None
        self.toPos = None
        self.ai = AI()
    
    def update(self):
        self.board.drawUI(self.win)
        if self.selectedPiece is not None:
            self.drawValidMoves(self.validMoves)    
        if self.selectedPiece is None:
            hasWon, who = self.winner()
            if hasWon:
                print(f"{who} has won the game!")
                sys.exit()
            if self.fromPos != None:
                self.drawMoveLine(self.fromPos, self.toPos)
        display.update()

    def drawValidMoves(self, validMoves):
        for move in validMoves:
            # print(move)
            r, c = move
            draw.circle(self.win, REDDIRECTION, (c * SQUARE_SIZE + SQUARE_SIZE//2, r * SQUARE_SIZE + SQUARE_SIZE//2), 13)
            draw.line(self.win, REDDIRECTION, (self.selectedPiece.col * SQUARE_SIZE + SQUARE_SIZE//2, self.selectedPiece.row * SQUARE_SIZE + SQUARE_SIZE//2), (c * SQUARE_SIZE + SQUARE_SIZE//2, r * SQUARE_SIZE + SQUARE_SIZE//2), 8)
            
    def drawMoveLine(self, fromPos, toPos):
        r0, c0 = fromPos
        r1, c1 = toPos
        draw.circle(self.win, BLUELINE, (c1 * SQUARE_SIZE + SQUARE_SIZE//2, r1 * SQUARE_SIZE + SQUARE_SIZE//2), 13)
        draw.line(self.win, BLUELINE, (c0 * SQUARE_SIZE + SQUARE_SIZE//2, r0 * SQUARE_SIZE + SQUARE_SIZE//2), (c1 * SQUARE_SIZE + SQUARE_SIZE//2, r1 * SQUARE_SIZE + SQUARE_SIZE//2), 8)
    
    def select(self, r, c):
        if self.selectedPiece is None:
            self.selectValidPiece(r, c)
            self.fromPos = (r, c)
        else:
            if (r, c) in self.validMoves:
                if self.board.getPiece(r, c) != -1 and self.board.getPiece(r, c).id == self.op:
                    self.board.removePiece(r, c)
                self.board.move(self.selectedPiece, r, c)
                self.toPos = (r, c)
                self.changeTurn()
            elif self.board.boardList2d[r][c]!=-1 and self.board.boardList2d[r][c].id == self.selectedPiece.id:
                self.selectValidPiece(r, c)
                fromPos = (r, c)
                
    def selectValidPiece(self, r, c):
        p = self.board.getPiece(r, c)
        if p != -1 and p.id == self.turn:
            self.selectedPiece = p
            self.validMoves = self.board.getValidMoves(p.row, p.col)
    
    def changeTurn(self):
        print(f"turn changed to {self.op}")
        self.validMoves.clear()
        self.selectedPiece = None
        if self.turn == BLACKID:
            self.turn = WHITEID
            self.op = BLACKID
            self.update()
            if AImode: self.ai.AImove(self)
            
        else:
            self.turn = BLACKID
            self.op = WHITEID
            
    def winner(self):
        return self.board.winner()

    
