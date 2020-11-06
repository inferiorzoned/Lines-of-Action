import pygame as pg
import math 
from .constants import *
from .board import *

class AI:
    def __init__(self):
        self.boardAI = Board()
        self.depth = 2
        self.ownid = 'W'
        self.opid = 'B'
        pass

    def AImove(self, game):
        for r in range(ROWS):
            for c in range(COLS):
                self.boardAI.simpleBoard[r][c] = game.board.simpleBoard[r][c]
        # print(self)
        # game.select(5, 0)
        # game.update()
        # print(self.boardAI.getValidMoves(5, 0))
        # s = game.board.getValidMoves(5, 0)  
        # r,c = s.pop()
        # game.select(r,c)
        
        afterMoveBoard = self.alphaBetaMiniMax()
        printBoard(afterMoveBoard)
        
        fromPos = None
        toPos = None 
        for r in range(ROWS):
            for c in range(COLS):
                if game.board.simpleBoard[r][c] == 'W' and afterMoveBoard[r][c] != 'W':
                    fromPos = (r, c)
                elif game.board.simpleBoard[r][c] != 'W' and afterMoveBoard[r][c] == 'W':
                    toPos = (r, c)
        r1, c1 = toPos
        r0, c0 = fromPos
        game.select(r0, c0)
        game.update()
        game.select(r1, c1)
                
        # self.boardAI.simpleMove(5, 0, 4, 6)
        # printBoard(self.getConfig())
        # self.boardAI.simpleMove(4, 6, 5, 0)
        # printBoard(self.getConfig())
    def getSuccessors(self, boardConfig, id):
        configs = []
        initPositions = []
        for r in range(ROWS):
            for c in range(COLS):
                if boardConfig[r][c] == id:
                    initPositions.append((r, c))
                    
        for r in range(ROWS):
            for c in range(COLS):
                self.boardAI.simpleBoard[r][c] = boardConfig[r][c]
                
        for pos in initPositions:
            r0, c0 = pos 
            for pos2 in self.boardAI.getValidMoves(r0, c0):
                r1, c1 = pos2
                if boardConfig[r][c] != '_': boardConfig[r][c] = '_'
                self.boardAI.simpleMove(r0, c0, r1, c1)
                configs.append(self.getConfig())
                # print(configs)
                self.boardAI.simpleMove(r1, c1, r0, c0)
        return configs 
    
        
    def alphaBetaMiniMax(self):
        maxVal, boardConfig = self.alphaBetaMax(self.depth, self.getConfig(), -math.inf, math.inf)
        return boardConfig
    
    def alphaBetaMax(self, depth, boardConfig, alpha, beta):
        # TODO or game over
        if depth == 0:  
            return self.eval(boardConfig), boardConfig 
        
        v = -math.inf
        configs = self.getSuccessors(boardConfig, 'W')
        print(len(configs))
        newBoard = None
        
        for possibleConfig in configs:
            val, confg = self.alphaBetaMin(depth-1, possibleConfig, alpha, beta)
            
            v = max(v, val)
            
            if v > beta:
                print("here")
                return v, boardConfig
            alpha = max(alpha, v)
            newBoard = [list(x) for x in possibleConfig]
        return v, newBoard
    
    def alphaBetaMin(self, depth, boardConfig, alpha, beta):
        # TODO or game over
        if depth == 0:  
            return self.eval(boardConfig), boardConfig 
        
        v = math.inf
        configs = self.getSuccessors(boardConfig, 'B')
        print(len(configs))
        newBoard = None
        
        for possibleConfig in configs:
            val, confg = self.alphaBetaMax(depth-1, possibleConfig, alpha, beta)
            v = min(v, val)
            
            if v < alpha:
                return v, boardConfig
            beta = min(beta, v)
            newBoard = [list(x) for x in possibleConfig]
        return v, newBoard
        
    
    def eval(self, boardConfig):
        return 0
    
    def getConfig(self):
        config = []
        for r in range(ROWS):
            config.append([])
            for c in range(COLS):
                config[r].append(self.boardAI.simpleBoard[r][c])
        return config
    
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
               
               
               
               
                
                
            