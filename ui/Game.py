from utils.Utils import Utils
from services.GameService import GameService
from services.Minimax import Minimax
from constants import Constants
import random
import math


class UI:

    @staticmethod
    def play(board):
        gameOver = False
        turn = random.randint(Constants.PLAYER, Constants.COMPUTER)
        while not gameOver:
            # Computer turn
            if turn == Constants.COMPUTER and not gameOver:
                col, score = Minimax.minimax(board, Constants.DEPTH, -math.inf, math.inf, True)

                if GameService.isValidPosition(board, col):
                    row = GameService.getNextEmptyPositionOnColumn(board, col)
                    GameService.dropPiece(board, row, col, Constants.COMPUTER)

                    if GameService.isWinningMove(board, Constants.COMPUTER):
                        print("Computer wins!")
                        gameOver = True

                    if GameService.fullBoard(board):
                        print("Draw!")
                        gameOver = True
                    Utils.printBoard(board)

                    turn = Constants.PLAYER
            else:
                # Ask for player input
                while turn == Constants.PLAYER and not gameOver:

                    col = input('Column: ')
                    try:
                        col = int(col)

                        if col >= Constants.COLUMN_COUNT:
                            print("Column is not in range " + '0 - ' + str(Constants.COLUMN_COUNT))
                        elif GameService.isValidPosition(board, col):
                            row = GameService.getNextEmptyPositionOnColumn(board, col)
                            GameService.dropPiece(board, row, col, Constants.PLAYER)

                            if GameService.isWinningMove(board, Constants.PLAYER):
                                print("Hurray, you won !")
                                gameOver = True

                            if GameService.fullBoard(board):
                                print("Draw!")
                                gameOver = True

                            turn = Constants.COMPUTER
                            Utils.printBoard(board)
                    except ValueError:
                        print("Wrong input")
