# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 14:22:01 2022

@author: AMenaya

TicTacToe program. To run:
from TicTacToe import TicTacToe
TicTacToe.play()
"""
import numpy as np
from itertools import groupby
from random import randint

BOARD_SIZE = 3
BLANK = " "
PLAYER_X = "X"
PLAYER_O = "O" 

class Board:
    def __init__(self, rows, cols):
        self.height = rows
        self.width = cols
        self.board = np.array([[BLANK]*self.width]*self.height)
        
    def resetBoard(self):
        self.board = np.array([[BLANK]*self.width]*self.height)
        return self
        
    def isBoardFull(self):
        return BLANK not in self.board
    
    def isSpotFull(self, coordinate):
        row = (coordinate - 1) //self.width
        col = (coordinate - 1) % self.width
        return self.board[row][col] != BLANK
        
    def updateBoard(self, player, coordinate): 
        row = (coordinate - 1) //self.width
        col = (coordinate - 1) % self.width
        self.board[row][col] = player
        return self
        
    def draw(self):
        b = self.board
        print(" -" + self.width * "-------")
        for row in range(self.height):
            for col in range(self.width):
                coord = row * self.width + col + 1
                print(" |"+ str(coord) + "  " + (1- (coord>9))*" " + (1- (coord>99))*" ", end = '')
            print(" |")
            for col in range(self.width):
                print(" |  " + b[row][col] +"  ", end = '')
            print(" |")
            print(" -" + self.width* "-------")
            
class Player:
    def __init__(self, token):
        self.token = token
        self.wins = 0
        
    def updWins(self):
        self.wins += 1
        return self
        
class MNKGame:
    def __init__(self, rows = 3, cols = 3, toWin = 3, token_1 = PLAYER_X, token_2 = PLAYER_O):
        """ m,n,k-game: m rows, n columns, k in line to win. TocTacToe = 3,3,3-game.
        Parameters:
        ----------
        rows    (int) -> (m) Number of rows
        columns (int) -> (n) Number of columns
        toWin   (int) -> (k) Number of consecutive tokens to win
        Returns
        -------
        MNKGame object. To play MNKGame().play()"""
        self.height = rows
        self.width = cols
        self.board = Board(rows, cols)
        self.player1 = Player(token_1)
        self.player2 = Player(token_2)
        self.activePlayer = self.selectRandomPlayer()
        self.toWin = toWin
        self.isThereWinner = False
        self.draw = False
    
    def selectRandomPlayer(self):
        r = randint(0,1)
        return self.player1.token*r + self.player2.token*(1-r)
    
    def swapPlayerTurn(self, player):
        r = self.player1.token == player
        self.activePlayer = self.player1.token*r + self.player2.token*(1-r)
        return self
    
    def isIterableFull(self, iterable):
        return BLANK not in iterable
    
    def allIterableEqual(self, iterable):
        g = groupby(iterable)
        return next(g, True) and not next(g, False)
    
    def kInLine(self, coordinate):
        """ Checks, given a coordinate, if there is a line with the given coordinate
        that has now k tokens in a row"""
        kInLine = False
        b = self.board
        row = (coordinate - 1) //b.width
        col = (coordinate - 1) % b.width
        
        bo = b.board
        # Check horizontal: each row
        all_spots_hor = range(max(0,col-self.toWin + 1),min(col+self.toWin,self.width))
        num_spots_hor = len(all_spots_hor) - self.toWin + 1
        print("horizontal " +str(num_spots_hor))
        for index_col in range(num_spots_hor):
            to_check = [[row, max(0,col-self.toWin + 1)+index_col + k] for k in range(self.toWin)]
            #print(to_check)
            #kInLine = kInLine or (self.isIterableFull(to_check) and self.allIterableEqual(to_check))
        # Check veritcal
        all_spots_ver = range(max(0,row-self.toWin + 1),min(row+self.toWin,self.height))
        num_spots_ver = len(all_spots_ver) - self.toWin + 1
        print("vertical "+str(num_spots_ver))
        for index_row in range(num_spots_ver):
            to_check = [[max(0,row-self.toWin + 1)+index_row + k, col] for k in range(self.toWin)]
            #print(to_check)
            #kInLine = kInLine or (self.isIterableFull(to_check) and self.allIterableEqual(to_check))
        # Check principal diagonal
        number_of_pd = ((self.width-(row-col)>=self.toWin-1) and (self.width-(col-row)>=self.toWin-1))*min(row+1, col+1, self.height-row, self.width-col, self.width-(row-col)-self.toWin+1,self.width-(col-row)-self.toWin+1, self.toWin)
        print("principal diagonal " + str(number_of_pd))
        for ind in range(number_of_pd):
            #This is not working 
            to_check = [[max(0, row-self.toWin) + ind + k, max(0, col-self.toWin) + ind + k] for k in range(self.toWin)]
            print(to_check)
            #kInLine = kInLine or (self.isIterableFull(to_check) and self.allIterableEqual(to_check))
        # Check secondary diagonal
        # Clean next line (because i changed j -> len -j and we can cancel stuff)
        number_of_sd = ((self.width-(row-(self.width-col-1))>=self.toWin-1) and (self.width-((self.width-col-1)-row)>=self.toWin-1))*min(row+1, (self.width-col-1)+1, self.height-row, self.width-(self.width-col-1), self.width-(row-(self.width-col-1))-self.toWin+1,self.width-((self.width-col-1)-row)-self.toWin+1, self.toWin)
        print(" antidiagonal " + str(number_of_sd))
        for ind in range(number_of_sd):
            # This is not right
            to_check = [[self.height + (max(0, row-self.toWin) - ind - k) - 1, self.width + (max(0, (self.width-col-1)-self.toWin) - ind - k) -1] for k in range(self.toWin)]
            print(to_check)
            #kInLine = kInLine or (self.isIterableFull(to_check) and self.allIterableEqual(to_check))
        return kInLine
        
    def play(self):
        # Reset board
        self.board.resetBoard()
        self.isThereWinner = False
        self.draw = False
        while not self.isThereWinner or self.draw:
            print("It is turn for player: " + self.activePlayer)
            # Show the board
            self.board.draw()
            # Ask user for a spot
            spots = str(self.width*self.height+1)
            inputSpot = int(input("Choose a spot < " + spots + ": "))
            while self.board.isSpotFull(inputSpot) or inputSpot > self.width*self.height+1 or inputSpot < 0:
                inputSpot = int(input("Invalid spot. Choose an empty spot < " + spots + ": "))
            self.board.updateBoard(self.activePlayer, inputSpot)
            self.isThereWinner = self.kInLine(inputSpot)
            self.draw = self.board.isBoardFull()
            self.swapPlayerTurn(self.activePlayer)
        
        self.swapPlayerTurn(self.activePlayer)
        msgWinner = "Winner is player " + self.activePlayer
        msgDraw = "Board is full, game ends in a draw"
        msg = msgWinner*self.isThereWinner + msgDraw*self.board.draw
        print(msg)