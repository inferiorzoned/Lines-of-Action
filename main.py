# import pygame as pg
from pygame import time, display, event, QUIT, MOUSEBUTTONDOWN, mouse
from LOA.constants import FPS, WIDTH, HEIGHT, SQUARE_SIZE
from LOA.game import *


WIN = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Lines of Action')

def mouseOnBoard(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
# run = True
def main():
    # global run
    run = True
    clk = time.Clock()
    game = Game(WIN)
    
    while run:
        clk.tick(FPS)

        for e in event.get():
            if e.type == QUIT:
                run = False
            
            if e.type == MOUSEBUTTONDOWN:
                pos = mouse.get_pos()
                row, col = mouseOnBoard(pos)
                game.select(row, col)
        
        game.update()
        
if __name__ == "__main__":
    main()

