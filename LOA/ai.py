# import pygame as pg
from math import inf
from copy import deepcopy
from .constants import ROWS, COLS
from .board import Board

class AI:
    def __init__(self):
        self.boardAI = Board()
        self.depth = 3
        self.ownid = 'W'
        self.opid = 'B'
        pass

    def AImove(self, game):
        self.boardAI.simpleBoard = [list(x) for x in game.board.simpleBoard]
        print(self.eval(self.getConfig()))
        
        afterMoveBoard = self.alphaBetaMiniMax()
        printBoard(afterMoveBoard)
        
        fromPos = toPos = None
        for r in range(ROWS):
            for c in range(COLS):
                if game.board.simpleBoard[r][c] == 'W' and afterMoveBoard[r][c] != 'W':
                    fromPos = (r, c)
                elif game.board.simpleBoard[r][c] != 'W' and afterMoveBoard[r][c] == 'W':
                    toPos = (r, c)
        r0, c0 = fromPos    
        r1, c1 = toPos
        game.select(r0, c0)
        # game.update()
        game.select(r1, c1)
        # print(self.eval(self.getConfig()))

    def getSuccessors(self, boardConfig, id):
        op = None
        if id == 'W': op = 'B'
        else: op = 'W'
        configs = []
        
        initPositions = [(r, c) for c in range(COLS) for r in range(ROWS) if boardConfig[r][c] == id]
        self.boardAI.simpleBoard =  [list(x) for x in boardConfig]
        for pos in initPositions:
            r0, c0 = pos 
            for pos2 in self.boardAI.getValidMoves(r0, c0):
                dummy = [list(x) for x in boardConfig]
                r1, c1 = pos2
                # if boardConfig[r][c] != '_': boardConfig[r][c] = '_'
                if dummy[r1][c1] != '_' and dummy[r1][c1] == op:
                    dummy[r1][c1] = '_'
                dummy[r0][c0], dummy[r1][c1] = dummy[r1][c1], dummy[r0][c0]
                dummyCopy = [list(x) for x in dummy]
                configs.append(dummyCopy)
                dummy[r0][c0], dummy[r1][c1] = dummy[r1][c1], dummy[r0][c0]
        return configs 
    
        
    def alphaBetaMiniMax(self):
        maxVal, boardConfig = self.alphaBetaMax(self.depth, self.getConfig(), -inf, inf)
        return boardConfig
    
    def alphaBetaMax(self, depth, boardConfig, alpha, beta):
        # TODO or game over
        if depth == 0:  
            return self.eval(boardConfig), boardConfig 
        
        v = -inf
        configs = self.getSuccessors(boardConfig, 'W')
        newBoard = None
        
        for possibleConfig in configs:
            val, confg = self.alphaBetaMin(depth-1, possibleConfig, alpha, beta)
            
            v = max(v, val)
            
            if v > beta:
                # return v, boardConfig
                return v, confg
            alpha = max(alpha, v)
            newBoard = [list(x) for x in possibleConfig]
        return v, newBoard
    
    def alphaBetaMin(self, depth, boardConfig, alpha, beta):
        # TODO or game over
        if depth == 0:  
            return self.eval(boardConfig), boardConfig 
        
        v = inf
        configs = self.getSuccessors(boardConfig, 'B')
        newBoard = None
        
        for possibleConfig in configs:
            val, confg = self.alphaBetaMax(depth-1, possibleConfig, alpha, beta)
            v = min(v, val)
            
            if v < alpha:
                # return v, boardConfig
                return v, confg
            beta = min(beta, v)
            newBoard = [list(x) for x in possibleConfig]
        return v, newBoard
        
    
    def eval(self, boardConfig):
        score = 0
        
        whitePieces = sum(line.count('W') for line in boardConfig)
        blackPieces = sum(line.count('B') for line in boardConfig)
        score += whitePieces - blackPieces
        
        return score
                
    def getConfig(self):
        return [list(x) for x in self.boardAI.simpleBoard]
    
    def __str__(self):
        str = ""
        for r in range(ROWS):
            for c in range(COLS):
                str += self.boardAI.simpleBoard[r][c] + " "
            str += "\n"
        return str 
    
def printBoard(config):
    str = ""
    for r in range(ROWS):
        for c in range(COLS):
            str += config[r][c] + " "
        str += "\n"
    print(str)
               
               
               
               
                
                
            