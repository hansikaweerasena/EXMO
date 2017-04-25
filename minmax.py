#!/usr/bin/env python

import random
from draw import plot

import argparse

parser = argparse.ArgumentParser(description='This is a basic gcode sender. http://crcibernetica.com')
parser.add_argument('-p','--port',help='Input USB port',required=True)
args = parser.parse_args()


class Tic(object):
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    winners = ('O-win', 'Draw', 'X-win')

    def __init__(self, squares=[]):
        if len(squares) == 0:
            self.squares = [None for i in range(9)]
        else:
            self.squares = squares

    def show(self):
        print('-------------------')
        print(' ' + str(self.squares[6]) + ' | ' + str(self.squares[7]) + ' | ' + str(self.squares[8]))
        print('-------------------')
        print(' ' + str(self.squares[3]) + ' | ' + str(self.squares[4]) + ' | ' + str(self.squares[5]))
        print('-------------------')
        print(' ' + str(self.squares[0]) + ' | ' + str(self.squares[1]) + ' | ' + str(self.squares[2]))
        print('-------------------')

    def available_moves(self):
        """what spots are left empty?"""
        return [k for k, v in enumerate(self.squares) if v is None]

    def available_combos(self, player):
        """what combos are available?"""
        return self.available_moves() + self.get_squares(player)

    def complete(self):
        """is the game over?"""
        if None not in [v for v in self.squares]:
            return True
        if self.winner() != None:
            return True
        return False

    def X_won(self):
        return self.winner() == 'O'

    def O_won(self):
        return self.winner() == 'X'

    def tied(self):
        return self.complete() == True and self.winner() is None

    def winner(self):
        for player in ('O', 'X'):
            positions = self.get_squares(player)
            for combo in self.winning_combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return None

    def get_squares(self, player):
        """squares that belong to a player"""
        return [k for k, v in enumerate(self.squares) if v == player]

    def make_move(self, position, player):
        """place on square on the board"""
        self.squares[position] = player

    def alphabeta(self, node, player, alpha, beta):
        if node.complete():
            if node.X_won():
                return -1
            elif node.tied():
                return 0
            elif node.O_won():
                return 1
        for move in node.available_moves():
            node.make_move(move, player)
            val = self.alphabeta(node, get_enemy(player), alpha, beta)
            node.make_move(move, None)
            if player == 'X':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == 'X':
            return alpha
        else:
            return beta


def determine(board, player):
    a = -2
    choices = []
    if len(board.available_moves()) == 9:
        return 4
    for move in board.available_moves():
        board.make_move(move, player)
        val = board.alphabeta(board, get_enemy(player), -2, 2)
        board.make_move(move, None)
        print "move:", move + 1, "causes:", board.winners[val + 1]
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)


def get_enemy(player):
    if player == 'O':
        return 'X'
    return 'O'

def getPlayerMove(previousBoard):
    # newBoard = kobbs()
    # while (previousBoard == newBoard):
    #     newBoard = kobbs()
    # for i in range(0,9):
    #     if(previousBoard[i] == None):
    #         if(newBoard[i]=='X'):
    #             return i
    return 10

def getfile(x):
    return {
        0 : '1.g',
        1 : '2.g',
        2 : '3.g',
        3 : '4.g',
        4 : '5.g',
        5 : '6.g',
        6 : '7.g',
        7 : '8.g',
        8 : '9.g'
    }[x]

def drawMove(move,port):
  fileName =getfile(move)
  plot(fileName,port)

def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

if __name__ == "__main__":
    board = Tic()
    board.show()

    turn = whoGoesFirst()
    if(turn == 'player'):
        print ("You makes the first move")
    else:
        print ("I makes the first move")
    while not board.complete():
        if(turn =='player'):
            player = 'O'
            # player_move = getPlayerMove(board.squares)
            player_move = int(raw_input("Your Move -: "))-1
            if not player_move in board.available_moves():
                continue
            board.make_move(player_move, player)
            board.show()
            turn = 'computer'
        else:    
            if board.complete():
                break
            player = 'X'
            computer_move = determine(board, player)
            board.make_move(computer_move, player)
            # drawMove(computer_move,args.port)
            board.show()
            turn = 'player'
    print "winner is", board.winner()