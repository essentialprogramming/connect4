from constants import Constants


class Matrix:
    DIRECTIONS = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    @staticmethod
    def transposeMatrix(m):
        # return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
        return list(zip(*m))

    @staticmethod
    def rotateRight(matrix):
        return list(zip(*matrix[::-1]))

    @staticmethod
    def rotateLeft(matrix):
        return list(zip(*matrix))[::-1]

    @staticmethod
    def rotate180(matrix):
        return list((matrix[::-1]))

    @staticmethod
    def subMatrix(matrix, row1, column1, row2, column2):
        return [[matrix[i][j] for j in range(column1, column2 + 1)] for i in range(row1, row2 + 1)]

    @staticmethod
    def insertMatrix(matrix, subMatrix, row, column):
        for index_row in range(0, len(subMatrix)):
            for index_column in range(0, len(subMatrix[0])):
                if not Matrix.isEmpty(subMatrix, index_row, index_column):
                    matrix[index_row + row][index_column + column] = subMatrix[index_row][index_column]

    @staticmethod
    def insertMatrixAtPosition(matrix, subMatrix, row, column, rowInSubMatrix, columnInSubMatrix):
        """
        Position (rowInSubMatrix, columnInSubMatrix) on (row, column) in matrix.
        Insert subMatrix relative to that position.
        """
        for index_row in range(0, len(subMatrix)):
            for index_column in range(0, len(subMatrix[0])):
                if not Matrix.isEmpty(subMatrix, index_row, index_column):
                    matrix[index_row + row - rowInSubMatrix][index_column + column - columnInSubMatrix] = \
                        subMatrix[index_row][index_column]

    @staticmethod
    def fitsInGrid(matrix, subMatrix, row, column, rowInSubMatrix, columnInSubMatrix):
        for index_row in range(0, len(subMatrix)):
            for index_column in range(0, len(subMatrix[0])):
                try:
                    Matrix.checkIsInRange(matrix, index_row + row - rowInSubMatrix,
                                          index_column + column - columnInSubMatrix)
                except IndexError as indexError:
                    return False
        return True

    @staticmethod
    def checkIsInRange(matrix, row, column):
        row = int(row)
        column = int(column)

        if row < 0 or row > len(matrix) - 1 or column > len(matrix) - 1 or column < 0:
            raise IndexError("The position is out of range. The position must be between the boundaries of the " +
                             str(len(matrix)) + " x " + str(len(matrix[0])) + " board")

        return True

    @staticmethod
    def isOverlapping(matrix, subMatrix, row, column, rowInSubMatrix, columnInSubMatrix):
        for index_row in range(0, len(subMatrix)):
            for index_column in range(0, len(subMatrix[0])):
                if not Matrix.isEmpty(matrix, index_row + row - rowInSubMatrix,
                                      index_column + column - columnInSubMatrix) \
                        and not Matrix.isEmpty(subMatrix, index_row, index_column):
                    return True
        return False

    @staticmethod
    def getCoordinatesInternal(matrix, subMatrix, row, column, rowInSubMatrix, columnInSubMatrix):
        """
        Position (rowInSubMatrix, columnInSubMatrix) on (row, column) in matrix.
        Insert subMatrix relative to that position.
        """
        for index_row in range(0, len(subMatrix)):
            for index_column in range(0, len(subMatrix[0])):
                if not Matrix.isEmpty(subMatrix, index_row, index_column):
                    yield index_row + row - rowInSubMatrix, index_column + column - columnInSubMatrix

    @staticmethod
    def getCoordinates(matrix, subMatrix, row, column, rowInSubMatrix, columnInSubMatrix):
        return list(Matrix.getCoordinatesInternal(matrix, subMatrix, row, column, rowInSubMatrix, columnInSubMatrix))

    @staticmethod
    def isEmpty(board, row, column):
        if board[row][column] == Constants.EMPTY:
            return True
        return False

    @staticmethod
    def direction(row, column, secondRow, secondColumn):
        if row == secondRow and secondColumn > column:
            return Matrix.DIRECTIONS.get("right")

        if row == secondRow and secondColumn < column:
            return Matrix.DIRECTIONS.get("left")

        if column == secondColumn and row > secondRow:
            return Matrix.DIRECTIONS.get("up")

        if column == secondColumn and row < secondRow:
            return Matrix.DIRECTIONS.get("down")
