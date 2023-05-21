import traceback
import pygame

from game import Game

try:
    pygame.init()
    g = Game()
    g.run()
except (Exception,):
    traceback.print_exc()
    input()
finally:
    pygame.display.quit()
    pygame.quit()

#python .\main.py schemas\schema0.txt words\words0.txt Backtracking
#python .\main.py schemas\schema4.txt words\words4.txt ArcConsistency
#python .\main.py schemas\schema0.txt words\words0.txt ArcConsistency