import pygame as pg
from .constants import *
from .board import *

class Game:
    def __init__(self, win):
        self.board = Board()
        self.selectedPiece = None
        self.turn = BLACKID
        self.op = WHITEID
        self.validMoves = set()
        self.win = win
    
    def update(self):
        self.board.drawUI(self.win)
        if self.selectedPiece is not None:
            self.drawValidMoves(self.validMoves)    
        if self.selectedPiece is None:
            hasWon, who = self.winner()
            if hasWon:
                print(f"{who} has won the game!")
        pg.display.update()

    def drawValidMoves(self, validMoves):
        for move in validMoves:
            # print(move)
            r, c = move
            pg.draw.circle(self.win, REDDIRECTION, (c * SQUARE_SIZE + SQUARE_SIZE//2, r * SQUARE_SIZE + SQUARE_SIZE//2), 13)
            pg.draw.line(self.win, REDDIRECTION, (self.selectedPiece.col * SQUARE_SIZE + SQUARE_SIZE//2, self.selectedPiece.row * SQUARE_SIZE + SQUARE_SIZE//2), (c * SQUARE_SIZE + SQUARE_SIZE//2, r * SQUARE_SIZE + SQUARE_SIZE//2), 8)
    
    def select(self, r, c):
        if self.selectedPiece is None:
            self.selectValidPiece(r, c)
        else:
            if (r, c) in self.validMoves:
                if self.board.getPiece(r, c) != -1 and self.board.getPiece(r, c).id == self.op:
                    self.board.removePiece(r, c)
                self.board.move(self.selectedPiece, r, c)
                self.changeTurn()
            elif self.board.boardList2d[r][c]!=-1 and self.board.boardList2d[r][c].id == self.selectedPiece.id:
                self.selectValidPiece(r, c)
                
    def selectValidPiece(self, r, c):
        p = self.board.getPiece(r, c)
        if p != -1 and p.id == self.turn:
            self.selectedPiece = p
            self.validMoves = self.board.getValidMoves(p)
    
    def changeTurn(self):
        print(f"turn changed to {self.op}")
        self.validMoves.clear()
        self.selectedPiece = None
        if self.turn == BLACKID:
            self.turn = WHITEID
            self.op = BLACKID
            # self.aiMove()
        else:
            self.turn = BLACKID
            self.op = WHITEID
            
    def winner(self):
        return self.board.winner()

    
