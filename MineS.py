import random, pygame, sys, math
from math import sqrt
from pygame.locals import *
pygame.init()
FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 800 # size of window's width in pixels
WINDOWHEIGHT = 900 # size of windows' height in pixels
BORDERHEIGHT = 700
BOXBORDER = 5
SQUARESWIDE= 26
SQUARESTALL = 26
SQUARESIZE = sqrt((WINDOWWIDTH*WINDOWWIDTH)/(SQUARESTALL * SQUARESWIDE))
RED = (255,0,0)
DARKRED=(155,0,0)
GRAY     = (100, 100, 100)
LIGHTGRAY = (160,160,160)
YELLOW   = (255, 255,   0)
BLACK = (0,0,0)
NUMFONT = pygame.font.Font('freesansbold.ttf', 20)
ENDFONT = pygame.font.Font('freesansbold.ttf', 100)
NUMSQUARES = SQUARESWIDE * SQUARESTALL
NUMMINES = (1/8) * NUMSQUARES
def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Mine Sweeper')
    gameboard = Board()
    gamePlay = True
    while True:
        leftMouseClicked = False
        rightMouseClicked = False
        firtClick = True
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN and event.button == BUTTON_LEFT:
                mousex, mousey = event.pos
                leftMouseClicked = True
            elif event.type == MOUSEBUTTONDOWN and event.button == BUTTON_RIGHT:
                mousex, mousey = event.pos
                rightMouseClicked = True
        boxx, boxy = gameboard.getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if gameboard.board[boxx][boxy].isBomb and leftMouseClicked and gamePlay:
                gameboard.board[boxx][boxy].click()
                gameboard.board[boxx][boxy].drawBomb()
                gamePlay = False
                for x in range(SQUARESWIDE):
                    for y in range(SQUARESTALL):
                        if gameboard.board[x][y].isBomb:
                            gameboard.board[x][y].drawBomb()
                gameboard.drawLines()
                endText = ENDFONT.render('GAME OVER', True, DARKRED)
                DISPLAYSURF.blit(endText, (75, 10))
                pygame.display.update()
            if gameboard.board[boxx][boxy].isBomb != True and leftMouseClicked and gamePlay:
                gameboard.recursiveClick(boxx, boxy)
                gameboard.drawLines()
            if rightMouseClicked and gamePlay:
                gameboard.board[boxx][boxy].click()
                gameboard.board[boxx][boxy].drawFlag()
                pygame.display.update()
                gameboard.drawLines()
            if gameboard.hasWon():
                gamePlay = False
class Square:

    def __init__ (self, xcorner, ycorner):
        self.x = xcorner
        self.y = ycorner
        self.isClicked = False
        self.isBomb = False
        self.numBomb =0
        self.hasFlag = False
        self.rect = pygame.Rect((self.x, self.y, SQUARESIZE, SQUARESIZE))
        pygame.draw.rect(DISPLAYSURF, GRAY, self.rect)
        self.nearMines =0
    def makeBomb(self):
        self.isBomb = True
        self.numBomb =1
    def click(self):
        self.isClicked = True
    def drawBomb(self):
        pygame.draw.rect(DISPLAYSURF, RED, self.rect)
    def drawFlag(self):
        pygame.draw.rect(DISPLAYSURF, YELLOW, self.rect)
        self.hasFlag = True
    def drawNum(self):
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, self.rect)
        if self.nearMines != 0:
            numText = NUMFONT.render(str(self.nearMines), True, BLACK)
            DISPLAYSURF.blit(numText, (self.x +9, self.y +8))
class Board:
    def __init__(self):
        tempx =0
        tempy =100
        self.board = []
        for x in range(SQUARESWIDE):
            column = []
            for y in range(SQUARESTALL):
                column.append(Square(tempx, tempy))
                tempy += SQUARESIZE
            tempx += SQUARESIZE
            tempy = 100
            self.board.append(column)
        tempMines = NUMMINES
        rand1 =0
        rand2 =0
        while tempMines > 0:
             rand1 = (random.randrange(0, SQUARESTALL-1, 1))
             rand2 = (random.randrange(0, SQUARESWIDE-1, 1))
             if self.board[rand1][rand2].isBomb != True:
                 self.board[rand1][rand2].makeBomb()
                 tempMines -= 1
        self.board[0][0].nearMines = self.board[0][1].numBomb + self.board[1][0].numBomb + self.board[1][1].numBomb

        self.board[0][SQUARESTALL-1].nearMines = self.board[0][SQUARESTALL-2].numBomb + self.board[1][SQUARESTALL-1].numBomb + self.board[1][SQUARESTALL-2].numBomb

        self.board[SQUARESWIDE-1][SQUARESTALL-1].nearMines = self.board[SQUARESWIDE-1][SQUARESTALL - 2].numBomb + self.board[SQUARESWIDE-2][SQUARESTALL-1].numBomb + self.board[SQUARESWIDE-2][SQUARESTALL - 2].numBomb

        self.board[SQUARESWIDE-1][0].nearMines = self.board[SQUARESWIDE-1][1].numBomb + self.board[SQUARESWIDE-2][0].numBomb + self.board[SQUARESWIDE-2][1].numBomb
        tempy =0
        for x in range(1, SQUARESWIDE-1, 1):
            self.board[x][tempy].nearMines = self.board[x+1][tempy].numBomb + self.board[x-1][tempy].numBomb + self.board[x][tempy+1].numBomb + self.board[x+1][tempy+1].numBomb + self.board[x-1][tempy+1].numBomb
        tempy = SQUARESTALL-1
        for x in range(1, SQUARESWIDE-1, 1):
            self.board[x][tempy].nearMines = self.board[x+1][tempy].numBomb + self.board[x-1][tempy].numBomb + self.board[x][tempy-1].numBomb + self.board[x+1][tempy-1].numBomb + self.board[x-1][tempy-1].numBomb
        tempx =0
        for y in range (1, SQUARESTALL-1,1):
            self.board[tempx][y].nearMines = self.board[tempx+1][y].numBomb + self.board[tempx-1][y].numBomb + self.board[tempx][y+1].numBomb + self.board[tempx+1][y+1].numBomb + self.board[tempx-1][y+1].numBomb
        tempx = SQUARESWIDE-1
        for y in range(1, SQUARESTALL - 1, 1):
            self.board[tempx][y].nearMines = self.board[tempx - 1][y].numBomb + self.board[tempx - 1][y-1].numBomb + self.board[tempx][y - 1].numBomb + self.board[tempx][y +1].numBomb + self.board[tempx - 1][y + 1].numBomb
        for x in range(SQUARESWIDE-1):
             for y in range(SQUARESTALL-1):
                 self.board[x][y].nearMines = self.board[x + 1][y].numBomb + self.board[x - 1][y].numBomb + self.board[x][y+1].numBomb + self.board[x][y-1].numBomb
                 self.board[x][y].nearMines += self.board[x + 1][y+1].numBomb + self.board[x + 1][y-1].numBomb + self.board[x - 1][y+1].numBomb + self.board[x - 1][y-1].numBomb
        pygame.display.update()
        self.drawLines()
    def drawLines(self):
        for x in range(SQUARESWIDE):
            pygame.draw.line(DISPLAYSURF, BLACK, (x * SQUARESIZE, 100), (x*SQUARESIZE, SQUARESTALL * SQUARESIZE + 100), BOXBORDER)
        for y in range(SQUARESTALL):
            pygame.draw.line(DISPLAYSURF, BLACK, (0, y*SQUARESIZE+100), (SQUARESWIDE * SQUARESIZE, y*SQUARESIZE +100), BOXBORDER)

        pygame.display.update()

    def getBoxAtPixel(self, x, y):
        for boxx in range(SQUARESWIDE):
            for boxy in range(SQUARESTALL):
                left = self.board[boxx][boxy].x
                top = self.board[boxx][boxy].y
                boxRect = pygame.Rect(left, top, SQUARESIZE, SQUARESIZE)
                if boxRect.collidepoint(x, y):
                    return (boxx, boxy)
        return (None, None)
    def recursiveClick(self, x, y):
        if self.board[x][y].isClicked != True:
            self.board[x][y].click()
            if self.board[x][y].isBomb != True:
                self.board[x][y].drawNum()
                if self.board[x][y].nearMines == 0 :
                  if x-1 >= 0 :
                        self.recursiveClick(x-1,y)
                        if y+1 <= SQUARESTALL -1:
                            self.recursiveClick(x - 1, y + 1)
                        if y-1 >= 0:
                            self.recursiveClick(x-1, y-1)
                  if y-1 >=0:
                        self.recursiveClick(x, y-1)
                  if x+1 <= SQUARESWIDE - 1:
                        self.recursiveClick(x+1, y)
                        if y + 1 <= SQUARESTALL - 1:
                            self.recursiveClick(x+1, y+1)
                        if y-1 >= 0:
                            self.recursiveClick(x+1, y-1)
                  if y + 1 <= SQUARESTALL - 1:
                        self.recursiveClick(x, y+1)
    def hasWon(self):
        for x in range(SQUARESWIDE):
            for y in range(SQUARESTALL):
                if self.board[x][y].isBomb and self.board[x][y].hasFlag != True:
                    return False
                    break
        endText = ENDFONT.render('You Won!', True, YELLOW)
        DISPLAYSURF.blit(endText, (75, 10))
        pygame.display.update()
        return True



main()
