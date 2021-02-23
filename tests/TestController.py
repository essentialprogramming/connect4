import unittest
from copy import deepcopy

from utils.BoardUtils import BoardUtils
from utils.Matrix import Matrix
from utils.Utils import Utils
from services.GameService import GameService
from constants import Constants


class TestController(unittest.TestCase):
    def player_drop_piece_success(self):
        board = Utils.createBoard()
        GameService.dropPiece(board, 1, 1, Constants.PLAYER)
        # self.assertEqual(board[1, 1], Constants.PLAYER)
        self.assertEqual(board[1][1], Constants.PLAYER)

    def computer_drop_piece_success(self):
        board = Utils.createBoard()
        GameService.dropPiece(board, 1, 1, Constants.COMPUTER)
        # self.assertEqual(board[1, 1], Constants.COMPUTER)
        self.assertEqual(board[1][1], Constants.COMPUTER)

    def position_is_valid(self):
        board = Utils.createBoard()
        GameService.dropPiece(board, 1, 1, Constants.COMPUTER)
        self.assertTrue(GameService.isValidPosition(board, 1))

    def position_is_not_valid(self):
        board = Utils.createBoard()
        for i in range(Constants.ROW_COUNT):
            GameService.dropPiece(board, i, 1, Constants.COMPUTER)
        self.assertFalse(GameService.isValidPosition(board, 1))

    def is_not_winning_move(self):
        board = Utils.createBoard()
        self.assertFalse(GameService.isWinningMove(board, Constants.COMPUTER))

    def is_not_full_board(self):
        board = Utils.createBoard()
        self.assertFalse(GameService.fullBoard(board))

    def is_winning_move(self):
        board = Utils.createBoard()
        GameService.dropPiece(board, 0, 0, Constants.COMPUTER)
        GameService.dropPiece(board, 1, 1, Constants.COMPUTER)
        GameService.dropPiece(board, 2, 2, Constants.COMPUTER)
        GameService.dropPiece(board, 3, 3, Constants.COMPUTER)
        self.assertTrue(GameService.isWinningMove(board, Constants.COMPUTER))

    @staticmethod
    def matrix_operations():
        board = BoardUtils.createBoard(' ', 2, 3)
        board[0][0] = 0
        board[0][1] = 1
        board[0][2] = 2
        board[1][0] = 3
        board[1][1] = 4
        board[1][2] = 5

        board = TestController.createPlaneMatrix()
        board = BoardUtils.createBoard('X', 3, 3)
        BoardUtils.printBoardV3(board)
        BoardUtils.printBoardV3(Matrix.rotateLeft(board))
        BoardUtils.printBoardV3(Matrix.rotateRight(board))
        BoardUtils.printBoardV3(Matrix.rotate180(board))
        BoardUtils.printBoardV3(Matrix.transposeMatrix(board))
        BoardUtils.printBoardV3(Matrix.subMatrix(board, 0, 1, 1, 2))

        bigBoard = BoardUtils.createBoard(' ', 8, 8)
        Matrix.insertMatrixAtPosition(bigBoard, board, 1, 2, 1, 0)
        print("Random position :", BoardUtils.randomPosition(bigBoard))
        print("Overlap :", Matrix.isOverlapping(bigBoard, board, 2, 4, 0, 0))
        Matrix.insertMatrixAtPosition(bigBoard, board, 2, 4, 0, 0)
        # Matrix.insertMatrixAtPosition(bigBoard, Matrix.rotateLeft(board), 3, 0, 2, 0)
        # Matrix.insertMatrixAtPosition(bigBoard, Matrix.rotateRight(board), 3, 2, 0, 0)
        BoardUtils.printBoardV2(bigBoard, bigBoard, bigBoard)
        try:
            print(Matrix.checkIsInRange(bigBoard, 7, 7))
            print(Matrix.fitsInGrid(bigBoard, board, 1, 2, 1, 0))
        except Exception as valueError:
            Utils.handleException(valueError)

    def testAll(self):
        self.player_drop_piece_success()
        self.computer_drop_piece_success()
        self.position_is_valid()
        self.position_is_not_valid()
        self.is_not_winning_move()
        self.is_winning_move()
        self.is_not_full_board()
        self.matrix_operations()

    @staticmethod
    def createPlaneMatrix():
        """
        Creates the plane matrix for the up direction if it is another direction it will just rotate the matix
        What the matrix has to look like
        0 0 1 0 0
        1 1 1 1 1
        0 0 1 0 0
        0 1 1 1 0
        """
        plane_matrix = []
        unitary_list = [0] * 5
        for index in range(4):
            plane_matrix.append(deepcopy(unitary_list))
        plane_matrix[0][2] = 1
        plane_matrix[2][2] = 1
        for index in range(0, 5):
            plane_matrix[1][index] = 1
        for index in range(1, 4):
            plane_matrix[3][index] = 1
        return plane_matrix


if __name__ == '__main__':
    unittest.main()
