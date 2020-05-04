import pygame
from UserInterface import UserInterface

def main():

    obj = UserInterface()
    obj.gameLoop()
    pygame.quit()

if __name__ == '__main__':
    main()
