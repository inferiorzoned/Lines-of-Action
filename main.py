import pygame as pg
from LOA.constants import *
from LOA.board import *
from LOA.game import *


WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Lines of Action')

def mouseOnBoard(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    
    run = True
    clk = pg.time.Clock()
    game = Game(WIN)
    
    while run:
        clk.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                row, col = mouseOnBoard(pos)
                game.select(row, col)
        
        game.update()
        
if __name__ == "__main__":
    main()

