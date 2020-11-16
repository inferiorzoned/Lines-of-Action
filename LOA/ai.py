# import pygame as pg
from math import inf, hypot
import sys
from copy import deepcopy
from .constants import WHITEID, BLACKID, DIR, DIRECTIONS, DIRX, DIRY, Dims
from .board import Board
# from .game import Game

class AI:
    def __init__(self, dim):
        self.boardAI = Board(dim)
        self.depth = 3
        self.ownid = 'W'
        self.opid = 'B'
        self.dim = dim
        pass

    def AImove(self, game):
        self.boardAI.simpleBoard = [list(x) for x in game.board.simpleBoard]
        # print(self)
    
        afterMoveBoard = self.alphaBetaMiniMax()
        # printBoard(afterMoveBoard)
        
        fromPos = toPos = None
        for r in range(self.dim):
            for c in range(self.dim):
                if game.board.simpleBoard[r][c] == 'W' and afterMoveBoard[r][c] != 'W':
                    fromPos = (r, c)
                elif game.board.simpleBoard[r][c] != 'W' and afterMoveBoard[r][c] == 'W':
                    toPos = (r, c)
        r0, c0 = fromPos    
        r1, c1 = toPos
        game.select((Dims.SQUARE_SIZE * c0 + Dims.SQUARE_SIZE // 2, Dims.SQUARE_SIZE * r0 + Dims.SQUARE_SIZE // 2))
        # game.select(r0, c0)
        # game.update()
        # game.select(r1, c1)
        game.select((Dims.SQUARE_SIZE * c1 + Dims.SQUARE_SIZE // 2, Dims.SQUARE_SIZE * r1 + Dims.SQUARE_SIZE // 2))

    def getSuccessors(self, boardConfig, id):
        op = None
        if id == 'W': op = 'B'
        else: op = 'W'
        configs = []
        
        initPositions = [(r, c) for c in range(self.dim) for r in range(self.dim) if boardConfig[r][c] == id]
        
        for pos in initPositions:
            r0, c0 = pos 
        
            for pos2 in self.getValidMoves(r0, c0, boardConfig):
                dummy = [list(x) for x in boardConfig]
                r1, c1 = pos2
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
        hasWon, who = self.winner(boardConfig)
        if depth == 0 or hasWon:  
            return self.eval(boardConfig, depth), boardConfig 
        maxv = -inf
        configs = self.getSuccessors(boardConfig, 'W')
        newBoard = None
        for possibleConfig in configs:
            val, confg = self.alphaBetaMin(depth-1, possibleConfig, alpha, beta)
            if maxv < val:
                maxv = val
                newBoard = [list(x) for x in possibleConfig]
                alpha = max(alpha, maxv)
                if beta <= alpha: break
        return maxv, newBoard
    
    def alphaBetaMin(self, depth, boardConfig, alpha, beta):
        hasWon, who = self.winner(boardConfig)
        if depth == 0 or hasWon:  
            return self.eval(boardConfig, depth), boardConfig 
        minv = inf
        configs = self.getSuccessors(boardConfig, 'B')
        newBoard = None
        for possibleConfig in configs:
            val, confg = self.alphaBetaMax(depth-1, possibleConfig, alpha, beta)
            if minv > val:
                minv = val
                newBoard = [list(x) for x in possibleConfig]
                beta = min(beta, minv)
                if beta <= alpha: break
        return minv, newBoard
        
    
    def eval(self, boardConfig, depth):
        whitePieces = [(r, c) for c in range(self.dim) for r in range(self.dim) if boardConfig[r][c] == 'W']
        blackPieces = [(r, c) for c in range(self.dim) for r in range(self.dim) if boardConfig[r][c] == 'B']
        # -------------------------check winner-------------------------
        NoofWhitePieces = len(whitePieces)
        NoofBlackPieces = len(blackPieces)
        hasWon, who = self.winner(boardConfig)
        if who == WHITEID:

            return 10000 + depth
        elif who == BLACKID:

            return -10000 - depth
        # --------------------------------heuristic starts---------------------------
        score = 0
        # ----------------------------check remaining pieces----------------------
        score += (NoofWhitePieces - NoofBlackPieces)*10
        # ----------------------------calculate density----------------------------
        whiteCOMX = sum(r for (r, c) in whitePieces)/ NoofWhitePieces
        whiteCOMY = sum(c for (r, c) in whitePieces)/ NoofWhitePieces
        blackCOMX = sum(r for (r, c) in blackPieces)/ NoofBlackPieces
        blackCOMY = sum(c for (r, c) in blackPieces)/ NoofBlackPieces
        
        densityW = sum(hypot(whiteCOMX-r, whiteCOMY-c) for (r, c) in whitePieces)/ NoofWhitePieces
        densityB = sum(hypot(blackCOMX-r, blackCOMY-c) for (r, c) in blackPieces)/ NoofBlackPieces
        score += (densityB - densityW)*10
        # -------------------------calculate area-----------------------
        wx0 = wy1 = bx0 = by1 = -1
        wy0 = wx1 = by0 = bx1 = self.dim+1
        posn = 0
        t = 0
        for row in boardConfig:
            for col in row:
                if col == 'W':
                    wx0 = max(wx0, t)
                    wy0 = min(wy0, posn)
                    wx1 = min(wx1, t)
                    wy1 = max(wy1, posn)
                elif col == 'B':
                    bx0 = max(bx0, t)
                    by0 = min(by0, posn)
                    bx1 = min(bx1, t)
                    by1 = max(by1, posn)
                posn += 1
            posn = 0
            t += 1
        areaA = abs(wx0-wx1) * abs(wy1-wy0)
        areaB = abs(bx0-bx1) * abs(by1-by0)
        score += (areaB - areaA)*10
        # ---------------pieceSQuareTable--------------------------------
        whitePieceVal = sum(Dims.pieceSquaretable[r][c] for (r, c) in whitePieces)
        blackPieceVal = sum(Dims.pieceSquaretable[r][c] for (r, c) in blackPieces)
        score += (whitePieceVal - blackPieceVal)*2
        
        return score
                
    def getConfig(self):
        return [list(x) for x in self.boardAI.simpleBoard]
    
    def getValidMoves(self, r, c, boardConfig):
        validPositions = set()
        # for direction in DIRECTIONS:
        for direction in DIRECTIONS:
            dx = DIRX[direction]
            dy = DIRY[direction]
            piecesinBothPaths = self.getPiecesinPath(direction, r, c, boardConfig)
            if self.canJump(piecesinBothPaths, direction, r, c, boardConfig[r][c], dx, dy, boardConfig):
                if self.getOpponentPiecesInPath(piecesinBothPaths, direction, r, c, boardConfig[r][c], dx, dy, boardConfig) == 0:
                    validPositions.add((r + dx*piecesinBothPaths, c + dy*piecesinBothPaths))
                    
            dx = DIRX[direction+1]
            dy = DIRY[direction+1]
            if self.canJump(piecesinBothPaths, direction+1, r, c, boardConfig[r][c], dx, dy, boardConfig):
                if self.getOpponentPiecesInPath(piecesinBothPaths, direction+1, r, c, boardConfig[r][c], dx, dy, boardConfig) == 0:
                    validPositions.add((r + dx*piecesinBothPaths, c + dy*piecesinBothPaths))
        return validPositions       
            
            
    def getPiecesinPath(self, direction, r, c, boardConfig):
        return 1 + self.getNumbers(direction, r, c, boardConfig) + self.getNumbers(direction+1, r, c, boardConfig)

    def getNumbers(self, direction, currRow, currCol, boardConfig):
        numbers = 0
        dx = DIRX[direction]
        dy = DIRY[direction]
        currRow += dx
        currCol += dy
        while self.withinBoard(currRow, currCol):
            if boardConfig[currRow][currCol] != '_':
                numbers += 1
            currRow = currRow + dx
            currCol = currCol + dy
        return numbers
    
    def getOpponentPiecesInPath(self, jump, direction, currRow, currCol, id, dx, dy, boardConfig):
        opponentPieces = 0
        r = currRow + dx
        c = currCol + dy
        while jump > 1:
            if boardConfig[r][c] != '_' and boardConfig[r][c] != id:
                opponentPieces += 1
            r = r + dx
            c = c + dy
            jump = jump - 1
        return opponentPieces
    
    def canJump(self, jump, direction, currRow, currCol, id, dx, dy, boardConfig):
        r = currRow + dx*jump
        c = currCol + dy*jump
        if self.withinBoard(r, c) and (boardConfig[r][c] == '_' or boardConfig[r][c] != id):
            return True
        else: return False
    
    def winner(self, boardConfig):
        w = [(r, c) for c in range(self.dim) for r in range(self.dim) if boardConfig[r][c] == 'W']
        b = [(r, c) for c in range(self.dim) for r in range(self.dim) if boardConfig[r][c] == 'B']
        w = len(w)
        b = len(b)
        if w == 1:
            return True, WHITEID
        elif b == 1:
            return True, BLACKID
        BstartFromRow = BstartFromCol = WstartFromRow = WstartFromCol = None
        firstBlackFound = firstWhiteFound = False  
        posn = 0
        t = 0
        for row in boardConfig:
            for col in row:
                r = t
                c = posn
                if col != '_':
                    if col == 'B' and not firstBlackFound:
                        BstartFromRow = r
                        BstartFromCol = c    
                        firstBlackFound = True
                    elif col == 'W' and not firstWhiteFound:
                        WstartFromRow = r
                        WstartFromCol = c    
                        firstWhiteFound = True
                posn += 1
                if firstBlackFound and firstWhiteFound: break
            posn = 0
            t += 1
            if firstBlackFound and firstWhiteFound: break
        
        blacksConnected = self.winDFS(BstartFromRow, BstartFromCol, 'B', boardConfig)
        if blacksConnected == b:
            return True, BLACKID
        whitesConnected = self.winDFS(WstartFromRow, WstartFromCol, 'W', boardConfig)
        if whitesConnected == w:
            return True, WHITEID
        return False, -1
    
    def winDFS(self, i, j, id, boardConfig):
        connectedPieces = 0
        visited, stack = set(), [(i, j)]   
        while stack:
            i, j = stack.pop()
            for di, dj in DIR:
                dx = i + di
                dy = j + dj
                if self.withinBoard(dx, dy) and (dx, dy) not in visited and boardConfig[dx][dy] == id:
                    connectedPieces += 1
                    visited.add((dx, dy))
                    stack.append((dx, dy))
        return connectedPieces
    
    def __str__(self):
        str = ""
        for r in range(self.dim):
            for c in range(self.dim):
                str += self.boardAI.simpleBoard[r][c] + " "
            str += "\n"
        return str 

    def withinBoard(self, r, c):
        return r >= 0 and r < self.dim and c >= 0 and c < self.dim
  
    def printBoard(config):
        str = ""
        for r in range(self.dim):
            for c in range(self.dim):
                str += config[r][c] + " "
            str += "\n"
        print(str)