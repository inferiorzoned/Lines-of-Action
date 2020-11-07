import timeit
import numpy as np
from timeit import Timer
from copy import deepcopy
from itertools import chain
from collections import Counter
from math import sqrt, hypot

CHECK1 = 10
CHECK2 = 20

def test1():
    for r in range(10):
        (c1, c2) = (CHECK1, CHECK2) if r%2 == 0 else (CHECK2, CHECK1)    

def test2():    
    for r in range(10):
        if r%2 == 0: c1, c2 = CHECK1, CHECK2
        else: c1, c2 = CHECK2, CHECK1
# test2 is better than test1


def test3(a, b, c, d, x, y, z):
    d, e, f, g, p, q, r = a, b, c, d, x, y, z
        
def test4(a, b, c, d, x, y, z):
    d = a
    e = b
    f = c
    g = d
    p = x
    q = y
    r = z
# test4 is most of the time (70%) better than test3

def test5():
    x = 5
    y = 10
    temp = x
    x = y
    y = temp
    
def test6():
    x = 5
    y = 10
    x, y = y, x
# both are almost equal

X = [
    [0, 1, 1, 1, 1, 1, 1, 0],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [0, 1, 1, 1, 1, 1, 1, 0]
]
def test7():
    Y = []
    for r in range(len(X)):
        Y.append([])
        for c in range(len(X[r])):
            Y[r].append(X[r][c])
    # print(type(Y))
    
def test8():
    Y = [list(x) for x in X]
    # print(type(Y))
# test8()
    
def test9():
    Y = [[i for i in line] for line in X]
    
# test8 is whole lot faster than test7
# test8 is faster than test9

class A:
    def __init__(self):
        super().__init__()
        pass
    def inB(self):
        Y = [list(x) for x in X]
    def testCopy(self):
        Y = [list(x) for x in X]
a = A()
def test10():
    # a = A()
    a.inB()

def outB():
    Y = [list(x) for x in X]
def test11():
    outB()
# test11 slightly better than test10

def test12():
    Y = deepcopy(X)
a = A()
def test13():
    # a = A()
    a.testCopy()
# test13 much faster than test12

def test14():
    initPositions = []
    for r in range(8):
        for c in range(8):
            if X[r][c] == 2:
                initPositions.append((r, c))
def test15():
    initPositions = [(r, c) for c in range(8) for r in range(8) if X[r][c] == 2]
# test15 slightly better than test14

def test16():
    whitePieces = blackPieces = 0
    for r in range(8):
        for c in range(8):
            if X[r][c] == 2:
                whitePieces += 1
            elif X[r][c] == 1:
                blackPieces += 1
def test17():
    whitePieces = sum(line.count(2) for line in X)
    blackPieces = sum(line.count(1) for line in X)
# test17 much faster than test16

def test18():
    whiteX = whiteY = 0
    for r in range(8):
        for c in range(8):
            if X[r][c] == 2:
                whiteX += r
                whiteY += c
    # print(whiteY)
    
def test19():
    # whiteX = sum(index*row.count(2) for index, row in enumerate(X))
    whiteX = whiteY = 0
    posn = 0
    for row in X:
        for col in row:
            if col == 2: 
                whiteX += posn//8
                whiteY += posn%8
            posn += 1
    # print(whiteX)
# test19 better than test18

x1 = 1.0
y1 = 2.4
x2 = 5
y2 = 6
def test20():
    dist = sqrt((x2 - x1)**2 + (y2 - y1)**2)
def test21():
    dist = hypot(x2 - x1, y2 - y1)
#test21 always better than test20

def test22():
    whitePieces = []
    blackPieces = []
    whiteX = whiteY = blackX = blackY = 0
    posn = 0
    for row in X:
        for col in row:
            if col == 2: 
                whiteX = posn//8
                whiteY = posn%8
                whitePieces.append((whiteX, whiteY))
            elif col == 1:
                blackX = posn//8
                blackY = posn%8
                blackPieces.append((blackX, blackY))
            posn += 1
    print((whitePieces))
    whiteX = sum(r for (r, c) in whitePieces)
    whiteY = sum(c for r, c in whitePieces)
    blackX = sum(r for r, c in blackPieces)
    blackY = sum(c for r, c in blackPieces)
    print(whiteX)
# test22()

def test23():
    whitePieces = []
    blackPieces = []
    whiteX = whiteY = blackX = blackY = 0
    posn = 0
    for row in X:
        for col in row:
            if col == 2: 
                whiteX = posn//8
                whiteY = posn%8
                whitePieces.append((whiteX, whiteY))
            elif col == 1:
                blackX = posn//8
                blackY = posn%8
                blackPieces.append((blackX, blackY))
            posn += 1
            
    ROWS = 8
    wx0 = wy1 = bx0 = by1 = -1
    wy0 = wx1 = by0 = bx1 = 8+1
    posn = 0
    for row in X:
        for col in row:
            if col == '2':
                wx0 = max(wx0, posn//ROWS)
                wy0 = min(wy0, posn%ROWS)
                wx1 = min(wx1, posn//ROWS)
                wy1 = max(wy1, posn%ROWS)
            elif col == '1':
                bx0 = max(bx0, posn//ROWS)
                by0 = min(by0, posn%ROWS)
                bx1 = min(bx1, posn//ROWS)
                by1 = max(by1, posn%ROWS)
def test24():
    whitePieces = []
    blackPieces = []
    whiteX = whiteY = blackX = blackY = 0
    posn = 0
    for row in X:
        for col in row:
            if col == 2: 
                whiteX = posn//8
                whiteY = posn%8
                whitePieces.append((whiteX, whiteY))
            elif col == 1:
                blackX = posn//8
                blackY = posn%8
                blackPieces.append((blackX, blackY))
            posn += 1
            
    wx0, wx1 = max(whitePieces)[0], min(whitePieces)[0]
    wy1, wy0 = max(whitePieces)[1], min(whitePieces)[1]
    bx0, bx1 = max(blackPieces)[0], min(blackPieces)[0]
    by1, by0 = max(blackPieces)[1], min(blackPieces)[1]
    
def test25():
    whitePieces = []
    blackPieces = []
    whiteX = whiteY = blackX = blackY = 0
    posn = 0
    for row in X:
        for col in row:
            if col == 2: 
                whiteX = posn//8
                whiteY = posn%8
                whitePieces.append((whiteX, whiteY))
            elif col == 1:
                blackX = posn//8
                blackY = posn%8
                blackPieces.append((blackX, blackY))
            posn += 1
            
    wx0, wx1 = tuple(map(max, zip(*whitePieces))) 
    wy1, wy0 = tuple(map(min, zip(*whitePieces))) 
    bx0, bx1 = tuple(map(max, zip(*whitePieces))) 
    by1, by0 = tuple(map(min, zip(*whitePieces))) 
# test23 better than test24 better test25

setup = '''
from __main__ import test1
from __main__ import test2
from __main__ import test3
from __main__ import test4
from __main__ import test5
from __main__ import test6
from __main__ import test7
from __main__ import test8
from __main__ import test9
from __main__ import test10
from __main__ import test11
from __main__ import test12
from __main__ import test13
from __main__ import test14
from __main__ import test15
from __main__ import test16
from __main__ import test17
from __main__ import test18
from __main__ import test19
from __main__ import test20
from __main__ import test21
from __main__ import test23
from __main__ import test24
from __main__ import test25
'''
        
t1 = '''test1()'''
t2 = '''test2()'''
t3 = '''test3(1, 2, 3, 4, 5, 6, 7)'''
t4 = '''test4(1, 2, 3, 4, 5, 6, 7)'''
t5 = '''test5()'''
t6 = '''test6()'''
t7 = '''test7()'''
t8 = '''test8()'''
t9 = '''test9()'''
t10 = '''test10()'''
t11 = '''test11()'''
t12 = '''test12()'''
t13 = '''test13()'''
t14 = '''test14()'''
t15 = '''test15()'''
t16 = '''test16()'''
t17 = '''test17()'''
t18 = '''test18()'''
t19 = '''test19()'''
t20 = '''test20()'''
t21 = '''test21()'''
t23 = '''test23()'''
t24 = '''test24()'''
t25 = '''test25()'''


print(timeit.timeit(setup=setup,stmt = t23, number = 100000))
print(timeit.timeit(setup=setup,stmt = t24, number = 100000))
print(timeit.timeit(setup=setup,stmt = t25, number = 100000))




