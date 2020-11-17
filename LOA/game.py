# import pygame as pg
from pygame import display, draw, event, font, QUIT, Surface, Rect
import sys
from time import sleep
from .ai import AI
from .constants import *
from .board import Board

# import sys, os, inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)

button6 = button8 = None

class Game:
    
    def __init__(self, win):
        self.board = None
        self.selectedPiece = None
        self.turn = BLACKID
        self.op = WHITEID
        self.validMoves = set()
        self.win = win
        self.fromPos = None
        self.toPos = None
        self.ai = None
        self.gameStarted = False
        self.dim = None

    def update(self):
        if self.gameStarted == False:
            self.drawDimSelection()
            return
        self.board.drawUI(self.win)
        if self.selectedPiece is not None:
            # hasWon, who = self.winner()
            # if hasWon:
            #     display.update()
            #     self.drawWinScreen(who)
            self.drawValidMoves(self.validMoves)

        if self.selectedPiece is None:
            self.drawMoveLine(self.fromPos, self.toPos)
            hasWon, who = self.winner()
            if hasWon:
                display.update()
                self.drawWinScreen(who)
        display.update()
        
    def drawDimSelection(self):
        global button6, button8 
        Surface.fill(self.win, CHECK2)
        rectWidth = BUTTONHEIGHT * 1.6
        rectHeight = BUTTONHEIGHT
        button6 = Rect(WIDTH/2-rectWidth/2, HEIGHT/2-rectHeight/2-rectHeight/1.5, rectWidth, rectHeight)
        button8 = Rect(WIDTH/2-rectWidth/2, HEIGHT/2-rectHeight/2+rectHeight/1.5, rectWidth, rectHeight)
        draw.rect(self.win, CHECK1, button6)
        draw.rect(self.win, CHECK1, button8)
        font.init()
        f = font.SysFont('Arial', 60)
        text6 = f.render('6 X 6', False, BLACK)
        text8 = f.render('8 X 8', False, BLACK)
        Surface.blit(self.win, text6, (button6.left+text6.get_width()/2-10, button6.top+text6.get_height()/2+5))
        Surface.blit(self.win, text8, (button8.left+text8.get_width()/2-10, button8.top+text8.get_height()/2+5))
        display.update()

    def drawWinScreen(self, who):
        print(f"{who} has won the game!")
        sleep(2)
        Surface.fill(self.win, WINBG)
        while True:
            for e in event.get():
                if e.type == QUIT:
                    sys.exit()
            if who == BLACKID:
                draw.circle(self.win, WHITE,
                            (WIDTH//2, HEIGHT//2 - 150), 150+2)
                draw.circle(self.win, BLACK,
                            (WIDTH//2, HEIGHT//2 - 150), 150)
            else:
                draw.circle(self.win, BLACK,
                            (WIDTH//2, HEIGHT//2 - 150), 150+2)
                draw.circle(self.win, WHITE,
                            (WIDTH//2, HEIGHT//2 - 150), 150)
            self.win.blit(WINS, ((WIDTH//2 - 200, HEIGHT//2 + 50)))
            display.update()

    def drawValidMoves(self, validMoves):
        for move in validMoves:
            # print(move)
            r, c = move
            sqr = Dims.SQUARE_SIZE
            draw.circle(self.win, REDDIRECTION, (c * sqr +
                                                 sqr//2, r * sqr + sqr//2), 13)
            draw.line(self.win, REDDIRECTION, (self.selectedPiece.col * sqr + sqr//2, self.selectedPiece.row *
                                               sqr + sqr//2), (c * sqr + sqr//2, r * sqr + sqr//2), 8)

    def drawMoveLine(self, fromPos, toPos):
        if fromPos is not None and toPos is not None:
            r0, c0 = fromPos
            r1, c1 = toPos
            sqr = Dims.SQUARE_SIZE
            draw.circle(self.win, BLUELINE, (c1 * sqr + sqr//2, r1 * sqr + sqr//2), 13)
            draw.line(self.win, BLUELINE, (c0 * sqr + sqr//2, r0 * sqr + sqr//2), (c1 * sqr + sqr//2, r1 * sqr + sqr//2), 8)    
        
    
    def select(self, pos):
        if self.gameStarted == False:
            if button6.collidepoint(pos) or button8.collidepoint(pos):
                if button6.collidepoint(pos): self.dim = 6
                else: self.dim = 8    
                self.gameStarted = True
                Dims.generateDims(self.dim)
                self.board = Board(self.dim)
                self.ai = AI(self.dim)
                return 
            return
        r, c = mouseOnBoard(pos)
        if self.selectedPiece is None:
            selected = self.selectValidPiece(r, c)
            if selected: self.fromPos = (r, c)
        else:
            if (r, c) in self.validMoves:
                if self.board.getPiece(r, c) != -1 and self.board.getPiece(r, c).id == self.op:
                    self.board.removePiece(r, c)
                self.board.move(self.selectedPiece, r, c)
                self.toPos = (r, c)
                self.changeTurn()
            elif self.board.boardList2d[r][c] != -1 and self.board.boardList2d[r][c].id == self.selectedPiece.id:
                selected = self.selectValidPiece(r, c)
                if selected: self.fromPos = (r, c)

    def selectValidPiece(self, r, c):
        p = self.board.getPiece(r, c)
        if p != -1 and p.id == self.turn:
            self.selectedPiece = p
            self.validMoves = self.board.getValidMoves(p.row, p.col)
            return True
        return False

    def changeTurn(self):
        # print(f"turn changed to {self.op}")
        self.validMoves.clear()
        self.selectedPiece = None
        if self.turn == BLACKID:
            self.turn = WHITEID
            self.op = BLACKID
            self.update()
            if AImode:
                self.ai.AImove(self)
            # print(self.board.whites_left, self.board.blacks_left)
        else:
            self.turn = BLACKID
            self.op = WHITEID
            # print(self.board.whites_left, self.board.blacks_left)

    def winner(self):
        return self.board.winner()
    
def mouseOnBoard(pos):
    x, y = pos
    row = y // Dims.SQUARE_SIZE
    col = x // Dims.SQUARE_SIZE
    return row, col
