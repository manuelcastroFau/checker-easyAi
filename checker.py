# [[file:checker.org::*questions][questions:1]]
# !/usr/bin/env python3


# -----------------------------------------------------------
# Project 1 COP 4630 Intro to Ai
# Professor: Oge Marques
# Authors: Manuel Castro
#          Siddi Waheed
# (C) 2022 Florida Atlantic University 
# -----------------------------------------------------------



from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax, SSS
from easyAI import solve_with_iterative_deepening
import numpy as np
import colorama
from colorama import Fore 

# black_square
even = [0,2,4,6]
odd = [1,3,5,7]

# init
even_row = [(i,j) for i in even for j in odd]
odd_row = [(i,j) for i in odd for j in even]

black_squares = even_row + odd_row

class Checker(TwoPlayerGame):

    def __init__(self, players):
        self.players = players
        self.blank_board = np.zeros((8,8), dtype=object)

        # To fill array with spaces instead of zeros
        self.blank_board[:]=' '
        self.board = self.blank_board.copy()
        self.black_pieces = [
            (0,1), (0,3), (0,5), (0,7),
            (1,0), (1,2), (1,4), (1,6)
        ]
        self.white_pieces = [
            (6,1), (6,3), (6,5), (6,7),
            (7,0), (7,2), (7,4), (7,6)
        ]
        for i,j in self.black_pieces:
            self.board[i,j] = "B"
        for i,j in self.white_pieces:
            self.board[i,j] = "W"

        self.white_territory = [(7,0), (7,2), (7,4), (7,6)]
        self.black_territory = [(0,1), (0,3), (0,5), (0,7)]


        self.players[0].pos = self.white_pieces
        self.players[1].pos = self.black_pieces

        self.current_player = 2  # player 1 starts.

    def possible_moves_on_white_turn(self):

        table_pos = []
        old_new_piece_pos = []

        # board position before move
        board = self.blank_board.copy()
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l

        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player-1].pos:
            old_piece_pos = v

            step_pos = [(v[0]-1, v[1]-1), (v[0]-1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B","W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j))
                    else:
                        old_new_piece_pos.append((old_piece_pos,n))

        # board position after  move
        for i,j in old_new_piece_pos:
            #print(f"i = {i}")
            b = board.copy()
            b[i[0], i[1]] = ' ' # old position
            b[j[0], j[1]] = "W" # new position
            # print(b)
            table_pos.append(b)
            assert len(np.where(b != ' ')[0]) == 16, f"In possible_moves_on_white_turn(), there are {len(np.where(b != ' ')[0])} pieces on the board  \n {b}"


        self.board = board
        return table_pos

    def possible_moves_on_black_turn(self):
        table_pos = []
        old_new_piece_pos = []

        # board position before move
        board = self.blank_board.copy()
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l

        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
        for v in self.players[self.current_player-1].pos:
            old_piece_pos = v

            step_pos = [(v[0]+1, v[1]-1), (v[0]+1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B","W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j))
                    else:
                        old_new_piece_pos.append((old_piece_pos,n))

        # board position after  move

        for i,j in old_new_piece_pos:
            b = board.copy()
            b[i[0], i[1]] = ' '
            b[j[0], j[1]] = "B"
            table_pos.append(b)
            assert len(np.where(b != ' ')[0]) == 16, f"In possible_moves_on_black_turn(), there are {len(np.where(b != ' ')[0])} pieces on the board  \n {b}"

        self.board = board
        return table_pos

    def possible_moves(self):
        """
        """

        if self.current_player == 2:
            return self.possible_moves_on_black_turn()
        else:
            return self.possible_moves_on_white_turn()

    def get_piece_pos_from_table(self, table_pos):
        if self.current_player-1 == 0:
            x = np.where(table_pos == "W")
        elif self.current_player-1 == 1:
            x = np.where(table_pos == "B")
        else:
            raise ValueError("There can be at most 2 players.")

        assert len(np.where(table_pos != 0)[0]) == 16, f"In get_piece_pos_from_table(), there are {len(np.where(table_pos != 0)[0])} pieces on the board  \n {table_pos}"
        return [(i,j) for i,j in zip(x[0], x[1])]

    def make_move(self, pos):
        """
        assign pieces index of pos array to current player position.

        parameters
        -------
        pos = position of all pieces on the (8 x 8) boards. type numpy array.

        example of pos
        [[0,B,0,B,0,B,0,B],
         [B,0,B,0,B,0,B,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,W,0,W,0,W,0,W],
         [W,0,W,0,W,0,W,0]]
        ------
        """

        newpos_1 = [] #Arraylist to hold data for P1
        newpos_2 = [] #Arraylist to hold data for P2
        for i in range(8):
            for j in range(8):
                if pos[i,j] == "B": #Looking for Black pieces in the board
                    current_pos=(i,j)
                    newpos_2.append(current_pos) #appending list with new positions
                if pos[i,j] == "W": #Looking for White pieces in the board
                    current_pos=(i,j)
                    newpos_1.append(current_pos)#appending list with new positions

        
        self.players[0].pos = newpos_1 #Updating player positions
        self.players[1].pos = newpos_2 
        pass

    def lose(self):
        """
        black lose if white piece is in black territory
        white lose if black piece is in black territory
        """
        for i in range(8):
            if self.board[7,i] == "B": #if Black piece are in white territory
                print('Player Black Wins')
                return 1
        for i in range(8):
            if self.board[0,i] == "W": #if white pieces are in black territory
                print('Player White Wins')
                return 1
        pass

    def is_over(self):
        """
        game is over immediately when one player get one of its piece into opponent's territory.
        """
        return (self.possible_moves() == []) or self.lose()
        pass

    def show(self):
        """
        show 8*8 checker board.
        """
        # board position before move
        
        print('\n')
        board = self.blank_board.copy()
        print(Fore.RED) #set font color to make visivility easier
        print(f"player 1 positions = {self.players[0].pos}")
        print(f"player 2 positions = {self.players[1].pos}")
        print(Fore.WHITE)
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l
        
        print(Fore.GREEN)
        print(board)
        print('\n BEFORE MOVE from Current player \n')
        print(Fore.WHITE)

    def scoring(self):
       """
       win = 0
       lose = -100
       """
       return 0 if self.lose() else 100
       pass

if __name__ == "__main__":
    ai = Negamax(1) # The AI will think 13 moves in advance
    ai2 = Negamax(6,win_score=90)
    game = Checker( [ AI_Player(ai), AI_Player(ai) ] )
    print(Fore.BLUE +'Welcome to our version of Checkers')
    print(Fore.RED + 'Please Leave comments')
    print(Fore.WHITE)
    history = game.play()
    if game.lose():
        pass
    else: #draw #if both players are out of moves
        print("Looks like we have a draw.")

