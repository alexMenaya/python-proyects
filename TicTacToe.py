# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 14:22:01 2022

@author: AMenaya
"""
import numpy as np
from itertools import groupby
from random import randint

BLANK = "."
PLAYER_X = "X"
PLAYER_O = "O" 

class TicTacToe:
    def __init__(self, n = 3):
        self.size = n
        self.board = np.array([[BLANK]*n]*n)
        self.activePlayer = ""
    
    def resetBoard(self):
        self.board = np.array([[BLANK]*self.size]*self.size)
        
    def draw(self):
        """ Draw a rudimentary board"""
        print(" -" + self.size* "----")
        for row in self.board:
            for column in row:
                print(" | " + column, end = '')
            print(" |")
            print(" -" + self.size* "----")
        return 
    
    def isBoardFull(self):
        """ Returns True if there is no possible move"""
        return BLANK not in self.board
    
    def isIterableFull(self, iterable):
        """ Returns True if the iterable contains no empty spaces (-)"""
        return BLANK not in iterable
    
    def all_equal(self, iterable):
        """ Returns True if all the elements are equal to each other"""
        g = groupby(iterable)
        return next(g, True) and not next(g, False)
    
    def threeInLine(self):
        """ Returns True if there is a line full with the same token"""
        b = self.board
        
        # Check rows b[row_num,:]
        for row in range(self.size):
            if self.isIterableFull(b[row,:]) and self.all_equal(b[row,:]):
                return True
        # Check columns b[:,column]
        for col in range(self.size):
            if self.isIterableFull(b[:,col]) and self.all_equal(b[:,col]):
                return True
        # Check diagonals
        principal = [b[k][k] for k in range(self.size)]
        secondary = [b[k][-(k+1)] for k in range(self.size)]
        if (self.isIterableFull(principal) and self.all_equal(principal)):
            return True
        if (self.isIterableFull(secondary) and self.all_equal(secondary)):
            return True
        return False
    
    def startingPlayer(self):
        r = randint(0,1)
        return PLAYER_X*r+PLAYER_O*(1-r)
    
    def swapPlayer(self, player):
        return PLAYER_O if player == PLAYER_X else PLAYER_X
    
    def play(self):
        # Reset board
        self.resetBoard()
        # Choose player
        player = self.startingPlayer()
        while True:
            print("It is turn of player " + player)
            # Show the board
            self.draw()
            # Ask user for a spot
            invalidSpot = True
            while invalidSpot:
                input_row, input_col = map(int, input("Choose a spot x y| 0<=x,y<=2: " ).split())
                if self.board[input_row, input_col] == BLANK:
                    self.board[input_row, input_col] = player
                    invalidSpot = False;
                else :
                    input_row, input_col = map(int, input("Invalid spot. Choose a spot (x,y)| 0<=x,y<=2: " ).split())
            
            # check if there is a line, break
            if self.threeInLine():
                print("Winner is player " + player)
                self.draw()
                break
            # check if the board is empty
            if self.isBoardFull():
                print("Draw")
                self.draw()
                break
            player = self.swapPlayer(player)
        
    