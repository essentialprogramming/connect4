from constants import Constants as Constants


class GameService:

    @staticmethod
    def dropPiece(board, row, column, piece):
        """
        Given a board and a position on the board, make a move.
         :param board: Play board represented as a matrix (m,n)
         :param row: A row on the board
         :param column: A column on the board
         :param piece: A piece on the Play board represented as a matrix (m,n)
        """
        board[row][column] = piece

    @staticmethod
    def isValidPosition(board, column):
        """
        Given a board and a column on the board, return if a piece can be dropped on it or not.
          :param board: Play board represented as a matrix (m,n)
          :param column: A column on the board
          :return true/false
        """
        return board[Constants.ROW_COUNT - 1][column] == Constants.EMPTY

    @staticmethod
    def getValidPositions(board):
        """
        Given a board, return a list of valid columns for next move.
           :param board: Play board represented as a matrix (m,n)
           :return List of columns
        """
        validPositions = []
        for column in range(Constants.COLUMN_COUNT):
            if GameService.isValidPosition(board, column):
                validPositions.append(column)
        return validPositions

    @staticmethod
    def getNextEmptyPositionOnColumn(board, column):
        """
        Given a board and a column on the board, return first empty row.
          :param board: Play board represented as a matrix (m,n)
          :param column: A column on the board
          :return row
        """
        for row in range(Constants.ROW_COUNT):
            if board[row][column] == Constants.EMPTY:
                return row

    @staticmethod
    def isWinningMove(board, piece):
        """
        Check if next move wins the current game.
           :param board: Play board represented as a matrix (m,n)
           :param piece: A piece on the board
           :return true/false

        """
        # Check horizontal locations for win
        for column in range(Constants.COLUMN_COUNT - 3):
            for row in range(Constants.ROW_COUNT):
                if board[row][column] == board[row][column + 1] == board[row][column + 2] \
                        == board[row][column + 3] == piece:
                    return True

        # Check vertical locations for win
        for column in range(Constants.COLUMN_COUNT):
            for row in range(Constants.ROW_COUNT - 3):
                if board[row][column] == board[row + 1][column] == board[row + 2][column] \
                        == board[row + 3][column] == piece:
                    return True

        # Check diagonals
        for column in range(Constants.COLUMN_COUNT - 3):
            for row in range(Constants.ROW_COUNT - 3):
                if board[row][column] == board[row + 1][column + 1] == board[row + 2][column + 2] \
                        == board[row + 3][column + 3] == piece:
                    return True

        for column in range(Constants.COLUMN_COUNT - 3):
            for row in range(3, Constants.ROW_COUNT):
                if board[row][column] == board[row - 1][column + 1] == board[row - 2][column + 2] \
                        == board[row - 3][column + 3] == piece:
                    return True

    @staticmethod
    def isLastMove(board):
        return GameService.isWinningMove(board, Constants.PLAYER) \
               or GameService.isWinningMove(board, Constants.COMPUTER) or GameService.fullBoard(board)

    @staticmethod
    def fullBoard(board):
        return len(GameService.getValidPositions(board)) == 0
