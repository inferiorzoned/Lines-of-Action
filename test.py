import timeit
import numpy as np
from timeit import Timer

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

setup = '''
from __main__ import test1
from __main__ import test2
from __main__ import test3
from __main__ import test4
from __main__ import test5
from __main__ import test6
'''
        
t1 = '''test1()'''
t2 = '''test2()'''
t3 = '''test3(1, 2, 3, 4, 5, 6, 7)'''
t4 = '''test4(1, 2, 3, 4, 5, 6, 7)'''
t5 = '''test5()'''
t6 = '''test6()'''

# print(timeit.timeit(setup=setup,stmt = t5, number = 1000000))
# print(timeit.timeit(setup=setup,stmt = t6, number = 1000000))

a, b = (2, 5)
print(a, b)


abc = []
for r in range(8):
    abc.append([])
    for c in range(8):
        abc[r].append(2)
print(abc)

defg = [list(x) for x in abc]
print(defg)