#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install pygame')


# In[1]:


import pygame


# In[2]:


class MiniMax_Algorithm:
    def __init__(self, GameBoard):
        self.GameBoard = GameBoard

    def checkWin(self):
        # 1 = x won
        # 0 = tie
        # -1 = o won

        # win by row
        for row in range(3):
            if self.GameBoard[row][0] == self.GameBoard[row][1] and self.GameBoard[row][1] == self.GameBoard[row][2]:
                if self.GameBoard[row][0] == 'x':
                    return 1
                elif self.GameBoard[row][0] == 'o':
                    return -1

        # win by col
        for col in range(3):
            if self.GameBoard[0][col] == self.GameBoard[1][col] and self.GameBoard[1][col] == self.GameBoard[2][col]:
                if self.GameBoard[0][col] == 'x':
                    return 1
                elif self.GameBoard[0][col] == 'o':
                    return -1

        # win by diagonal
        if self.GameBoard[0][0] == self.GameBoard[1][1] and self.GameBoard[2][2] == self.GameBoard[1][1]:
            if self.GameBoard[1][1] == 'x':
                return 1
            elif self.GameBoard[1][1] == 'o':
                return -1
        if self.GameBoard[0][2] == self.GameBoard[1][1] and self.GameBoard[2][0] == self.GameBoard[1][1]:
            if self.GameBoard[1][1] == 'x':
                return 1
            elif self.GameBoard[1][1] == 'o':
                return -1

        for i in range(3):
            for j in range(3):
                if self.GameBoard[i][j] == '-':
                    return 2
        return 0

    def max(self):
        x = None
        y = None
        max_eval = -2
        status = self.checkWin()
        # print(Eval)
        if status != 2:
            return (status, 0, 0)
        for row in range(0, 3):
            for col in range(0, 3):
                if self.GameBoard[row][col] == '-':
                    self.GameBoard[row][col] = 'x'
                    min_eval = self.min()[0]
                    # print(min_eval)
                    if max_eval < min_eval:
                        max_eval = min_eval
                        x = col
                        y = row
                    self.GameBoard[row][col] = '-'
        return (max_eval, x, y)

    def min(self):
        x = None
        y = None
        min_eval = 2
        status = self.checkWin()
        # print(Eval)
        if status != 2:
            return (status, 0, 0)
        for row in range(0, 3):
            for col in range(0, 3):
                if self.GameBoard[row][col] == '-':
                    self.GameBoard[row][col] = 'o'
                    max_eval = self.max()[0]
                    # print(max_eval)
                    if min_eval > max_eval:
                        min_eval = max_eval
                        x = col
                        y = row
                    self.GameBoard[row][col] = '-'
        return (min_eval, x, y)


# In[1]:


class Game:
    def __init__(self):
        self.GameState = 2
        background_color = (0, 128, 128)
        self.foreground_color = (255, 255, 255)
        (width, height) = (900, 900)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Tic Tac Toe')
        self.screen.fill(background_color)
        pygame.display.flip()

    def drawBoard(self):
        # start - stop - step
        for xy in range(300, 601, 300):
            pygame.draw.line(self.screen, self.foreground_color,
                             (0, xy), (900, xy), 3)
            # start point - end point - width
            pygame.draw.line(self.screen, self.foreground_color,
                             (xy, 0), (xy, 900), 3)

    def drawX(self, x, y):
        x += 1
        y += 1
        pygame.draw.line(self.screen, self.foreground_color, (300 * x -
                                                              300 + 10, 300 * y - 300 + 10),
                         ((x * 300) - 10, (y * 300) - 10), 3)
        pygame.draw.line(self.screen, self.foreground_color, (300 * x - 300 + 10,
                                                              (y * 300) - 10), ((x * 300) - 10, 300 * y - 300 + 10), 3)

    def drawO(self, x, y):
        x += 1
        y += 1
        pygame.draw.circle(self.screen, self.foreground_color,
                           (x * 300 - 150, y * 300 - 150), 150, 3)

    def UI_for_game(self, gameboard):
        self.gameboard = gameboard

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    Mouse_x, Mouse_y = pygame.mouse.get_pos()
                    x = round(Mouse_x / 300 - 0.49)
                    y = round(Mouse_y / 300 - 0.49)
                    self.Return_GameOver()
                    if self.GameState == 2:
                        ValidMove = self.Move(x, y, 'o')
                        if ValidMove:
                            return self.gameboard
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.drawBoard()
            for row in range(3):
                for col in range(3):
                    if self.gameboard[row][col] == 'x':
                        self.drawX(col, row)
                    if self.gameboard[row][col] == 'o':
                        self.drawO(col, row)
            pygame.display.update()

    def Move(self, x, y, player):

        if self.gameboard[y][x] == '-':
            self.gameboard[y][x] = player
            return True
        return False

    def Return_GameOver(self):
        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        # my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.GameState = MiniMax_Algorithm(self.gameboard).checkWin()
        if self.GameState == 1:
            print('x Won this Game')

        elif self.GameState == 0:
            print('None Won')

        elif self.GameState == -1:
            print('o Won this Game')


# In[ ]:


if __name__ == "__main__":
    Board = [['-', '-', '-'],
             ['-', '-', '-'],
             ['-', '-', '-']]
    my_Game = Game()
    while True:
        my_Game.UI_for_game(Board)
        create = MiniMax_Algorithm(Board)
        bestmove = create.max()
        my_Game.Move(bestmove[1], bestmove[2], 'x')


# In[ ]:




