import re

from constants import Constants as Constants
from utils.BoardUtils import BoardUtils
from utils.Matrix import Matrix


class Utils:

    @staticmethod
    def parseCommand(inputCommand):
        """
        Separate the command and arguments
        :param inputCommand: string
        """
        inputCommand = inputCommand.lstrip(" ")
        position = inputCommand.find(" ")

        if position == -1:
            return inputCommand, []

        command = inputCommand[: position]
        # arguments = inputCommand[position + 1:].split()
        arguments = Utils.split(inputCommand[position + 1:])

        return command, arguments

    @staticmethod
    def createBoard():
        board = BoardUtils.createBoard(Constants.EMPTY, Constants.ROW_COUNT, Constants.COLUMN_COUNT)
        return board

    @staticmethod
    def printBoard(board):
        BoardUtils.printBoardV3(Matrix.rotate180(board))

    @staticmethod
    def split(inputString):
        def strip_quotes(s):
            if s and (s[0] == '"' or s[0] == "'") and s[0] == s[-1]:
                return s[1:-1]
            return s

        return [strip_quotes(p).replace('\\"', '"').replace("\\'", "'") \
                for p in re.findall(r'"(?:\\.|[^"])*"|\'(?:\\.|[^\'])*\'|[^\s]+', inputString)]

    @staticmethod
    def handleException(error):
        errorString = str(error) + ", please try again"
        print(errorString)
