from copy import deepcopy
import random

from texttable import Texttable

from constants import Constants


class BoardUtils:
    DIRECTIONS = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    @staticmethod
    def createBoard(initialValue, numberOfRows, numberOfColumns):
        board = [[initialValue for column in range(numberOfColumns)] for row in range(numberOfRows)]
        return board

    @staticmethod
    def column(board, column):
        return [row[column] for row in board]

    @staticmethod
    def row(board, row):
        return board[row][:]

    @staticmethod
    def isFullBoard(board):
        for row in range(BoardUtils.rowCount(board)):
            for column in range(BoardUtils.columnCount(board)):
                if board[row][column] == Constants.EMPTY:
                    return False
        return True

    @staticmethod
    def isEmpty(board, row, column):
        if board[row][column] == Constants.EMPTY:
            return True
        return False

    @staticmethod
    def count(board, element):
        counter = 0
        for row in range(BoardUtils.rowCount(board)):
            for column in range(BoardUtils.columnCount(board)):
                if board[row][column] == element:
                    counter += 1
        return counter

    @staticmethod
    def findElement(board, element):
        for row in range(len(board)):
            line = board[row]
            for column in range(len(line)):
                if board[row][column] == element:
                    return row, column
        return None

    @staticmethod
    def neighborsBoard(board, radius, rowNumber, columnNumber):
        return [[board[i][j] if 0 <= i < len(board) and 0 <= j < len(board[0]) else Constants.EMPTY
                 for j in range(columnNumber - radius, columnNumber + radius + 1)]
                for i in range(rowNumber - radius, rowNumber + radius + 1)]

    @staticmethod
    def neighborsList(board, radius, rowNumber, columnNumber):
        return [(row, column) for row in range(rowNumber - radius, rowNumber + radius + 1)
                for column in range(columnNumber - radius, columnNumber + radius + 1)
                if (0 <= row < len(board) and 0 <= column < len(board[0])
                    and (row != rowNumber or column != columnNumber))
                ]

    @staticmethod
    def surroundingIsEmpty(board, row, column):
        """
        Checks if the surrounding cells of a cell are taken
          :param board
          :param row
          :param column

        :return: false(if occupied) or true
        """

        neighboursList = list(BoardUtils.neighborsList(board, 1, row, column))
        for element in neighboursList:
            if not BoardUtils.isEmpty(board, element[0], element[1]):
                return False
        return True

    @staticmethod
    def surroundingContains(board, row, column, piece):
        """
        Checks if the surrounding cells of a cell contain a piece
          :param board
          :param row
          :param column
          :param piece

        :return: false(if contains) or true
        """

        neighboursList = list(BoardUtils.neighborsList(board, 1, row, column))
        for element in neighboursList:
            if board[element[0]][element[1]] == piece:
                return True
        return False

    @staticmethod
    def neighboursContains(board, row, column, piece):
        """
        Checks if the neighbour cells(left, right, up, down) of a cell contain a piece
          :param board
          :param row
          :param column
          :param piece

        :return: false(if contains) or true
        """

        neighboursList = []
        for rowIndex, columnIndex in BoardUtils.DIRECTIONS.values():
            if 0 <= row + rowIndex < len(board) and 0 <= column + columnIndex < len(board[0]):
                neighboursList.append((row + rowIndex, column + columnIndex))

        for rowIndex, columnIndex in neighboursList:
            if board[rowIndex][columnIndex] == piece:
                return True
        return False

    @staticmethod
    def emptyNeighborsList(board, row, column):
        """
        Neighbors as a list
          :param board
          :param row
          :param column
        """

        neighboursList = list(BoardUtils.neighborsList(board, 1, row, column))
        emptyNeighbours = []
        for row, column in neighboursList:
            if BoardUtils.isEmpty(board, row, column):
                emptyNeighbours.append((row, column))
        return emptyNeighbours

    @staticmethod
    def printTextTable(board):
        table = Texttable()
        table.add_rows(board, [])
        print(table.draw())

    @staticmethod
    def printBoardInternalV1(board):
        header = '   '.join(chr(ord('A') + i) for i in range(BoardUtils.columnCount(board))) + "   "
        grid = "    " + header
        rowNumber = 1
        for row in board:
            row = map(str, row)
            grid += "\n" + str(rowNumber) + "   " + "   ".join(row) + "   "
            rowNumber = rowNumber + 1
        return grid

    @staticmethod
    def printBoardInternalV2(board):
        header = '   '.join(str(i + 1) for i in range(BoardUtils.columnCount(board))) + "   "
        grid = "    " + header
        for index, row in enumerate(board):
            row = map(str, row)
            grid += "\n" + chr(ord('A') + index) + " | " + " | ".join(row) + " | "
        return grid

    @staticmethod
    def printBoardInternalV3(board):
        grid = '    '
        for index, row in enumerate(board):
            row = map(str, row)
            grid += "\n" + " | " + " | ".join(row) + " | "
        return grid

    @staticmethod
    def printBoardInternalV4(board):
        header = ""
        for columnIndex in range(BoardUtils.columnCount(board)):
            spacing = "   " if columnIndex < 9 else "  "
            header += str(columnIndex + 1) + spacing
        # header = '   '.join(str(i + 1) for i in range(BoardUtils.columnCount(board))) + "   "
        grid = "     " + header
        rowNumber = 1
        for row in board:
            row = map(str, row)
            spacing = "  | " if rowNumber < 10 else " | "
            grid += "\n" + str(rowNumber) + spacing + " | ".join(row) + " | "
            rowNumber = rowNumber + 1
        return grid

    @staticmethod
    def printBoard(*boards):
        splitBoard = []
        for board in boards:
            board_lines = BoardUtils.printBoardInternalV1(board).splitlines()
            splitBoard.append(board_lines)

        board = list(map('    '.join, zip(*splitBoard)))
        board = '\n'.join(board)
        print(board)

    @staticmethod
    def printBoardV2(*boards):
        splitBoard = []
        for board in boards:
            board_lines = BoardUtils.printBoardInternalV2(board).splitlines()
            splitBoard.append(board_lines)

        board = list(map('      '.join, zip(*splitBoard)))
        board = '\n'.join(board)
        print(board)

    @staticmethod
    def printBoardV3(*boards):
        splitBoard = []
        for board in boards:
            board_lines = BoardUtils.printBoardInternalV3(board).splitlines()
            splitBoard.append(board_lines)

        board = list(map('    '.join, zip(*splitBoard)))
        board = '\n'.join(board)
        print(board)

    @staticmethod
    def printBoardV4(*boards):
        splitBoard = []
        for board in boards:
            board_lines = BoardUtils.printBoardInternalV4(board).splitlines()
            splitBoard.append(board_lines)

        board = list(map('    '.join, zip(*splitBoard)))
        board = '\n'.join(board)
        print(board)

    @staticmethod
    def columnCount(board):
        return len(board[0])

    @staticmethod
    def rowCount(board):
        return len(board)

    @staticmethod
    def clone(board):
        return deepcopy(board)

    @staticmethod
    def getAllEmptyPositions(matrix):
        for index_row in range(0, len(matrix)):
            for index_column in range(0, len(matrix[0])):
                if BoardUtils.isEmpty(matrix, index_row, index_column):
                    yield index_row, index_column

    @staticmethod
    def randomPosition(board):
        return random.sample(list(BoardUtils.getAllEmptyPositions(board)), 1)[0]

    @staticmethod
    def randomCustomPosition(board, condition):
        candidates = [(row, column) for row, column in list(BoardUtils.getAllEmptyPositions(board)) if condition(row, column)]
        return random.sample(candidates, 1)[0]

    @staticmethod
    def positionWithMaxNumberOfNeighbours(board, element):
        rowIndex, columnIndex = BoardUtils.randomPosition(board)
        countNeighbours = 0
        emptyPositions = BoardUtils.getAllEmptyPositions(board)
        for row, column in emptyPositions:
            neighboursMatrix = BoardUtils.neighborsBoard(board, 1, row, column)
            if BoardUtils.count(neighboursMatrix, element) > countNeighbours:
                countNeighbours = BoardUtils.count(neighboursMatrix, element)
                rowIndex, columnIndex = row, column
        return rowIndex, columnIndex

    @staticmethod
    def randomEmptyNeighbour(board, row, column):
        if len(BoardUtils.emptyNeighborsList(board, row, column)) > 0:
            return random.sample(list(BoardUtils.emptyNeighborsList(board, row, column)), 1)[0]
        return BoardUtils.randomPosition(board)

    @staticmethod
    def isOverlapping(matrix, *coordinates):
        for row, column in coordinates:
            if not BoardUtils.isEmpty(matrix, row, column):
                return True
        return False

    @staticmethod
    def cleanCoordinates(matrix, *coordinates):
        for row, column in coordinates:
            if not BoardUtils.isEmpty(matrix, row, column):
                matrix[row][column] = Constants.EMPTY
