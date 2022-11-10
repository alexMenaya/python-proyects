# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 14:22:01 2022

@author: AMenaya

Some more tests

TicTacToe program. To run:
from TicTacToe import TicTacToe
TicTacToe.play()
"""
import numpy as np
from itertools import groupby
import random
from time import sleep

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
    def __init__(self, token, index, ai = False):
        self.token = token
        self.index = index
        self.ai = ai
        self.wins = 0
        
    def updWins(self):
        self.wins += 1
        return self
    
    def move(self, board):
        if self.ai:
            move = 0;
        else:
            spots = str(board.width*board.height+1)
            move = int(input("Choose a spot < " + spots + ": "))
            while board.isSpotFull(move) or move > board.width*board.height+1 or move < 0:
                 move = int(input("Invalid spot. Choose an empty spot < " + spots + ": "))
        return move;
        
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
        # Board
        self.height = rows
        self.width = cols
        self.board = Board(rows, cols)
        self.toWin = toWin
        # Players
        self.players = [Player(token_1, 0), Player(token_2, 1)]
        self.activePlayerIndex = random.randint(0,1)
        self.activePlayer = self.players[self.activePlayerIndex]
        # Endgame
        self.isThereWinner = False
        self.isDraw = False
    
    def swapPlayerTurn(self, playerIndex):
        r = self.activePlayerIndex == playerIndex
        self.activePlayer = self.players[0].token*(1-r) + self.players[1].token*r
        self.activePlayerIndex = not(playerIndex)
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
        for index_col in range(num_spots_hor):
            to_check = [bo[row, max(0,col-self.toWin + 1)+index_col + k] for k in range(self.toWin)]
            kInLine = kInLine or (self.isIterableFull(to_check) and self.allIterableEqual(to_check))
        
        # Check veritcal
        all_spots_ver = range(max(0,row-self.toWin + 1),min(row+self.toWin,self.height))
        num_spots_ver = len(all_spots_ver) - self.toWin + 1
        for index_row in range(num_spots_ver):
            to_check = [bo[max(0,row-self.toWin + 1)+index_row + k, col] for k in range(self.toWin)]
            kInLine = kInLine or (self.isIterableFull(to_check) and self.allIterableEqual(to_check))
        
        # Check principal diagonal
        number_of_pd = ((self.width-(row-col)>=self.toWin-1) and (self.width-(col-row)>=self.toWin-1))*min(row+1, col+1, self.height-row, self.width-col, self.width-(row-col)-self.toWin+1,self.width-(col-row)-self.toWin+1, self.toWin)
        for ind in range(number_of_pd): 
            to_check = [bo[row - min(row, col, self.toWin -1) + ind + k, col - min(row, col, self.toWin -1) + ind + k] for k in range(self.toWin)]
            kInLine = kInLine or (self.isIterableFull(to_check) and self.allIterableEqual(to_check))
        
        # Check secondary diagonal
        # Number of secondary diagonals is the number of first diagonals with col -> self.width -col -1
        number_of_sd = ((self.width-(row-(self.width-col-1))>=self.toWin-1) and (self.width-((self.width-col-1)-row)>=self.toWin-1))*min(row+1, (self.width-col-1)+1, self.height-row, self.width-(self.width-col-1), self.width-(row-(self.width-col-1))-self.toWin+1,self.width-((self.width-col-1)-row)-self.toWin+1, self.toWin)
        for ind in range(number_of_sd):
            to_check = [bo[row - min(row, (self.width-col-1), self.toWin -1) + ind + k, col + min(row, (self.width-col-1), self.toWin -1) - ind - k] for k in range(self.toWin)]
            kInLine = kInLine or (self.isIterableFull(to_check) and self.allIterableEqual(to_check))
        
        return kInLine
        
    def play(self):
        # Reset board
        self.board.resetBoard()
        self.isThereWinner = False
        self.isDraw = False
        while not (self.isThereWinner or self.isDraw):
            print("It is turn for player: " + self.activePlayer.token)
            # Show the board
            self.board.draw()
            # Ask user for a spot
            inputSpot = self.activePlayer.move(self.board)
            # Update board and check for winners            
            self.board.updateBoard(self.activePlayer.token, inputSpot)
            self.isThereWinner = self.kInLine(inputSpot)
            self.isDraw = self.board.isBoardFull()
            self.swapPlayerTurn(self.activePlayer.index)
        
        self.swapPlayerTurn(self.activePlayer)
        msgWinner = "Winner is player " + self.activePlayer
        msgDraw = "Board is full, game ends in a draw"
        msg = msgWinner*self.isThereWinner + msgDraw*self.isDraw
        print(msg)
        self.board.draw()
        
def main():
    # Here comes the code
    get_input_height = int(input("Number of rows: "))
    get_input_width = int(input("Number of columns: "))
    k_in_row = int(input("To win place k in a line. Choose k: "))
    game = MNKGame(rows = get_input_height, cols = get_input_width, toWin = k_in_row)
    game.play()
    while True:
        more = input("To quit insert q, to replay r: ")
        if more == "q":
            break
        elif more == "r":
            game.play()
    

# This I need to think it for the moment
if __name__ == '__main__':
    main()
    
    
