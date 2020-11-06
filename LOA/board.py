import pygame as pg
from .constants import *
from .piece import *

class Board:
    def __init__(self):
        self.boardList2d = []
        self.simpleBoard = []
        self.blacks_left = self.whites_left = 12
        self.addPiecesToBoard()
        
    def draw_checkBoard(self, win):
        for r in range(ROWS):
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
            self.simpleBoard.append([])
            for c in range(COLS):
                if r == 0 or r == ROWS-1:
                    if c!=0 and c!=COLS-1:
                        p = Piece(r, c, BLACK, BLACKID)
                        simplep = 'B'
                    else:
                        p = -1
                        simplep = '_'        
                else:
                    if c==0 or c==COLS-1:
                        p = Piece(r, c, WHITE, WHITEID)
                        simplep = 'W'
                    else:
                        p = -1
                        simplep = '_'        
                self.boardList2d[r].append(p)
                self.simpleBoard[r].append(simplep)
    
    def drawUI(self, win):
        self.draw_checkBoard(win)
        for r in range(ROWS):
            for c in range(COLS):
                p = self.boardList2d[r][c]
                if p != -1:
                    p.draw_piece(win)
                    
    def move(self, piece, r, c):
        self.simpleMove(piece.row, piece.col, r, c)
        self.boardList2d[piece.row][piece.col], self.boardList2d[r][c] = self.boardList2d[r][c], self.boardList2d[piece.row][piece.col]
        piece.update(r, c)
    
    def simpleMove(self, pr, pc, r, c):
        self.simpleBoard[pr][pc], self.simpleBoard[r][c] = self.simpleBoard[r][c], self.simpleBoard[pr][pc]
        
    def getValidMoves(self, r, c):
        validPositions = set()
        for direction in DIRECTIONS:
            dx = DIRX[direction]
            dy = DIRY[direction]
            piecesinBothPaths = self.getPiecesinPath(direction, r, c)
            if self.canJump(piecesinBothPaths, direction, r, c, self.simpleBoard[r][c], dx, dy):
                if self.getOpponentPiecesInPath(piecesinBothPaths, direction, r, c, self.simpleBoard[r][c], dx, dy) == 0:
                    validPositions.add((r + dx*piecesinBothPaths, c + dy*piecesinBothPaths))
            
            dx = DIRX[direction+1]
            dy = DIRY[direction+1]
            if self.canJump(piecesinBothPaths, direction+1, r, c, self.simpleBoard[r][c], dx, dy):
                if self.getOpponentPiecesInPath(piecesinBothPaths, direction+1, r, c, self.simpleBoard[r][c], dx, dy) == 0:
                    validPositions.add((r + dx*piecesinBothPaths, c + dy*piecesinBothPaths))
        return validPositions
    
    def getPiecesinPath(self, direction, r, c):
        return 1 + self.getNumbers(direction, r, c) + self.getNumbers(direction+1, r, c) 
    
    def getNumbers(self, direction, currRow, currCol):
        numbers = 0
        dx = DIRX[direction]
        dy = DIRY[direction]
        currRow = currRow + dx
        currCol = currCol + dy
        while withinBoard(currRow, currCol):
            if self.simpleBoard[currRow][currCol] != '_':
                numbers += 1
            currRow = currRow + dx
            currCol = currCol + dy
        return numbers
    
    def canJump(self, jump, direction, currRow, currCol, id, dx, dy):
        r = currRow + dx*jump
        c = currCol + dy*jump
        if withinBoard(r, c) and (self.simpleBoard[r][c] == '_' or self.simpleBoard[r][c] != id):
            return True
        else: return False
    
    def getOpponentPiecesInPath(self, jump, direction, currRow, currCol, id, dx, dy):
        opponentPieces = 0
        r = currRow + dx
        c = currCol + dy
        while jump > 1:
            if self.simpleBoard[r][c] != '_' and self.simpleBoard[r][c] != id:
                opponentPieces += 1
            r = r + dx
            c = c + dy
            jump = jump - 1
        return opponentPieces
    
    def getPiece(self, r, c):
        return self.boardList2d[r][c]
    
    def removePiece(self, r, c):
        if self.boardList2d[r][c].id == WHITEID:
            self.whites_left -= 1
        elif self.boardList2d[r][c].id == BLACKID:
            self.blacks_left -= 1
        self.boardList2d[r][c] = -1
        self.simpleBoard[r][c] = '_'
        
    def winner(self):
        if self.whites_left == 1:
            return True, WHITEID
        elif self.blacks_left == 1:
            return True, BLACKID
        BstartFromRow = BstartFromCol = WstartFromRow = WstartFromCol = None
        firstBlackFound = firstWhiteFound = False
        for r in range(ROWS):
            for c in range(COLS):
                if self.boardList2d[r][c] != -1:
                    if self.boardList2d[r][c].id == BLACKID and not firstBlackFound:
                        BstartFromRow = r
                        BstartFromCol = c    
                        firstBlackFound = True
                    elif self.boardList2d[r][c].id == WHITEID and not firstWhiteFound:
                        WstartFromRow = r
                        WstartFromCol = c    
                        firstWhiteFound = True
                if firstBlackFound and firstWhiteFound: break
            if firstBlackFound and firstWhiteFound: break
            
        blacksConnected = self.winDFS(BstartFromRow, BstartFromCol, BLACKID)
        if blacksConnected == self.blacks_left:
            return True, BLACKID
        whitesConnected = self.winDFS(WstartFromRow, WstartFromCol, WHITEID)
        if whitesConnected == self.whites_left:
            return True, WHITEID
        return False, -1
    
    def winDFS(self, i, j, id):
        connectedPieces = 0
        visited, stack = set(), [(i, j)]   
        while stack:
            i, j = stack.pop()
            for k in range(len(DIRX)):
                dx = i + DIRX[k]
                dy = j + DIRY[k]
                if withinBoard(dx, dy) and (dx, dy) not in visited and self.boardList2d[dx][dy]!=-1 and self.boardList2d[dx][dy].id == id:
                    connectedPieces += 1
                    visited.add((dx, dy))
                    stack.append((dx, dy))
        return connectedPieces
    
    def __str__(self):
        boardConfig = ""
        for r in range(ROWS):
            for c in range(COLS):
                if self.boardList2d[r][c] == -1: p = '_ '
                elif self.boardList2d[r][c].id == BLACKID: p = 'B '
                else: p = 'W '
                boardConfig += p
            boardConfig += "\n"
        return boardConfig