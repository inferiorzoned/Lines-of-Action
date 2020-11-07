# import pygame as pg
from math import inf, hypot
from copy import deepcopy
from .constants import ROWS, COLS, WHITEID, BLACKID
from .board import Board

class AI:
    def __init__(self):
        self.boardAI = Board()
        self.depth = 4
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
        whitePieces = []
        blackPieces = []
        whiteX = whiteY = blackX = blackY = 0
        posn = 0
        for row in boardConfig:
            for col in row:
                if col == 'W': 
                    whiteX = posn//ROWS
                    whiteY = posn%ROWS
                    whitePieces.append((whiteX, whiteY))
                elif col == 'B':
                    blackX = posn//ROWS
                    blackY = posn%ROWS
                    blackPieces.append((blackX, blackY))
                posn += 1
        # -------------------------check winner-------------------------
        self.boardAI.simpleBoard = [list(x) for x in boardConfig]
        hasWon, who = self.boardAI.winner()
        if who == WHITEID:
            return 10000
        elif who == BLACKID:
            return -10000
        score = 0
        # ----------------------------check remaining pieces----------------------
        NoofWhitePieces = len(whitePieces)
        NoofBlackPieces = len(blackPieces)
        score += (NoofWhitePieces - NoofBlackPieces)*10
        # ----------------------------calculate density----------------------------
        # whiteX = whiteY = blackX = blackY = 0
        # posn = 0
        whiteX = sum(r for (r, c) in whitePieces)
        whiteY = sum(c for (r, c) in whitePieces)
        blackX = sum(r for (r, c) in blackPieces)
        blackY = sum(c for (r, c) in blackPieces)
        # for row in boardConfig:
        #     for col in row:
        #         if col == 'W': 
        #             whiteX += posn//ROWS
        #             whiteY += posn%ROWS
        #         elif col == 'B':
        #             blackX += posn//ROWS
        #             blackY += posn%ROWS
        #         posn += 1
        whiteCOMX = whiteX/ NoofWhitePieces
        whiteCOMY = whiteY/ NoofWhitePieces
        blackCOMX = blackX/ NoofBlackPieces
        blackCOMY = blackY/ NoofBlackPieces
        # densityW = densityB = 0
        # posn = 0
        densityW = sum(hypot(whiteCOMX-r, whiteCOMY-c) for (r, c) in whitePieces)/ NoofWhitePieces
        densityB = sum(hypot(blackCOMX-r, blackCOMY-c) for (r, c) in blackPieces)/ NoofBlackPieces
        # for row in boardConfig:
        #     for col in row:
        #         if col == 'W': 
        #             whiteX = posn//ROWS
        #             whiteY = posn%ROWS
        #             densityW += hypot(whiteCOMX-whiteX, whiteCOMY-whiteY)
        #         elif col == 'B':
        #             blackX = posn//ROWS
        #             blackY = posn%ROWS
        #             densityB += hypot(blackCOMX-blackX, blackCOMY-blackY)
        #         posn += 1
        # densityW = densityW/ whitePieces
        # densityB = densityB/ blackPieces
        score += (densityB - densityW)*5
        # -------------------------calculate area-----------------------
        # wx0 = wy1 = bx0 = by1 = -1
        # wy0 = wx1 = by0 = bx1 = ROWS+1
        # posn = 0
        # for row in boardConfig:
        #     for col in row:
        #         if col == 'W':
        #             wx0 = max(wx0, posn//ROWS)
        #             wy0 = min(wy0, posn%ROWS)
        #             wx1 = min(wx1, posn//ROWS)
        #             wy1 = max(wy1, posn%ROWS)
        #         elif col == 'B':
        #             bx0 = max(bx0, posn//ROWS)
        #             by0 = min(by0, posn%ROWS)
        #             bx1 = min(bx1, posn//ROWS)
        #             by1 = max(by1, posn%ROWS)
        # areaA = abs(wx0-wx1) * abs(wy1-wy0)
        # areaB = abs(bx0-bx1) * abs(by1-by0)
        # score += (areaB - areaA)*2
        
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
               
               
               
               
                
                
            