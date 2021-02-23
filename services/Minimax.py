from copy import deepcopy

from services.GameService import GameService
from constants import Constants as Constants
import random
import math

from utils.BoardUtils import BoardUtils


class Minimax(GameService):
    """description of class"""

    @staticmethod
    def eval(line, piece):
        """
        Evaluation function
         :param line: A line on the Play board represented as a matrix (m,n)
         :param piece: A piece on the Play board represented as a matrix (m,n)

         :return: Computed score if next move would be the piece dropped on the board on given line
        """
        score = 0

        isPlayer = Constants.PLAYER == piece
        opponentPiece = (Constants.PLAYER, Constants.COMPUTER)[isPlayer]

        if line.count(piece) == 4:
            score += 100
        elif line.count(piece) == 3 and line.count(Constants.EMPTY) == 1:
            score += 3
        elif line.count(piece) == 2 and line.count(Constants.EMPTY) == 2:
            score += 2

        if line.count(opponentPiece) == 3 and line.count(Constants.EMPTY) == 1:
            score -= 4

        return score

    @staticmethod
    def score(board, piece):
        """
        Evaluation function
         :param board: Play board represented as a matrix (m,n)
         :param piece: A piece on the Play

         :return: Computed score(sum) for all possible actions.
        """
        score = 0

        # Score center column
        line = BoardUtils.column(board, Constants.COLUMN_COUNT // 2)
        center_count = line.count(piece)
        score += center_count * 3

        # Score Horizontal
        for rowIndex in range(Constants.ROW_COUNT):
            row = BoardUtils.row(board, rowIndex)
            for column in range(Constants.COLUMN_COUNT - Constants.CONDITION):
                line = row[column:column + Constants.LINE_LENGTH]
                score += Minimax.eval(line, piece)

        # Score Vertical
        for columnIndex in range(Constants.COLUMN_COUNT):
            column = BoardUtils.column(board, columnIndex)
            for row in range(Constants.ROW_COUNT - Constants.CONDITION):
                line = column[row:row + Constants.LINE_LENGTH]
                score += Minimax.eval(line, piece)

        # Score diagonal
        for row in range(Constants.ROW_COUNT - Constants.CONDITION):
            for column in range(Constants.COLUMN_COUNT - Constants.CONDITION):
                line = [board[row + i][column + i] for i in range(Constants.LINE_LENGTH)]
                score += Minimax.eval(line, piece)

        for row in range(Constants.ROW_COUNT - Constants.CONDITION):
            for column in range(Constants.COLUMN_COUNT - Constants.CONDITION):
                line = [board[row + Constants.CONDITION - i][column + i] for i in range(Constants.LINE_LENGTH)]
                score += Minimax.eval(line, piece)

        return score

    @staticmethod
    def minimax(board, depth, alpha, beta, maximizingPlayer):
        """
        Minimax algorithm for choosing the next move
           :param board: Play board represented as a matrix (m,n)
           :param depth: current depth in game tree
           :param alpha: The best (highest-value) choice we have found so far at any point along the path of Maximizer.
                         The initial value of alpha is -∞
           :param beta: The best (lowest-value) choice we have found so far at any point along the path of Minimizer.
                        The initial value of beta is +∞.
           :param maximizingPlayer: is true if current move is of maximizer, else false

           :return: column/ computed score
        """
        validPositions = GameService.getValidPositions(board)
        isLastPosition = GameService.isLastMove(board)
        if depth == 0 or isLastPosition:
            if isLastPosition:
                if GameService.isWinningMove(board, Constants.COMPUTER):
                    return None, math.inf
                elif GameService.isWinningMove(board, Constants.PLAYER):
                    return None, -math.inf
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, Minimax.score(board, Constants.COMPUTER)
        if maximizingPlayer:
            value = -math.inf
            chooseColumn = random.choice(validPositions)
            for column in validPositions:
                row = GameService.getNextEmptyPositionOnColumn(board, column)
                boardCopy = deepcopy(board)
                GameService.dropPiece(boardCopy, row, column, Constants.COMPUTER)
                newScore = Minimax.minimax(boardCopy, depth - 1, alpha, beta, False)[1]
                if newScore > value:
                    value = newScore
                    chooseColumn = column
                alpha = max(alpha, value)
                if alpha >= beta:  # Condition for Alpha-beta pruning
                    break
            return chooseColumn, value

        else:  # Minimizing player
            value = math.inf
            chooseColumn = random.choice(validPositions)
            for column in validPositions:
                row = GameService.getNextEmptyPositionOnColumn(board, column)
                boardCopy = deepcopy(board)
                GameService.dropPiece(boardCopy, row, column, Constants.PLAYER)
                newScore = Minimax.minimax(boardCopy, depth - 1, alpha, beta, True)[1]
                if newScore < value:
                    value = newScore
                    chooseColumn = column
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return chooseColumn, value
