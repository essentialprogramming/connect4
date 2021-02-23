import pygame
from pygame import gfxdraw
from utils.Utils import Utils
from services.GameService import GameService
from services.Minimax import Minimax
from constants import Constants
import sys
import random
import math


class GUI:
    SLOT_SIZE = 80
    RADIUS = int(SLOT_SIZE / 2 - 3)

    width = Constants.COLUMN_COUNT * SLOT_SIZE
    height = (Constants.ROW_COUNT + 1) * SLOT_SIZE
    size = (width, height)

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect four")
    pygame.init()

    @staticmethod
    def drawBoard(board):
        for column in range(Constants.COLUMN_COUNT):
            for row in range(Constants.ROW_COUNT):
                pygame.draw.rect(GUI.screen, Constants.BACKGROUND, (
                column * GUI.SLOT_SIZE, row * GUI.SLOT_SIZE + GUI.SLOT_SIZE, GUI.SLOT_SIZE, GUI.SLOT_SIZE))
                pygame.gfxdraw.aacircle(GUI.screen, int(column * GUI.SLOT_SIZE + GUI.SLOT_SIZE / 2),
                                        int(row * GUI.SLOT_SIZE + GUI.SLOT_SIZE + GUI.SLOT_SIZE / 2), GUI.RADIUS,
                                        Constants.BLACK)
                pygame.gfxdraw.filled_circle(GUI.screen, int(column * GUI.SLOT_SIZE + GUI.SLOT_SIZE / 2),
                                             int(row * GUI.SLOT_SIZE + GUI.SLOT_SIZE + GUI.SLOT_SIZE / 2), GUI.RADIUS,
                                             Constants.BLACK)
        for column in range(Constants.COLUMN_COUNT):
            for row in range(Constants.ROW_COUNT):
                if board[row][column] == Constants.PLAYER:
                    pygame.gfxdraw.aacircle(GUI.screen, int(column * GUI.SLOT_SIZE + GUI.SLOT_SIZE / 2),
                                            GUI.height - int(row * GUI.SLOT_SIZE + GUI.SLOT_SIZE / 2), GUI.RADIUS + 1,
                                            Constants.GREEN)
                    pygame.gfxdraw.filled_circle(GUI.screen, int(column * GUI.SLOT_SIZE + GUI.SLOT_SIZE / 2),
                                                 GUI.height - int(row * GUI.SLOT_SIZE + GUI.SLOT_SIZE / 2),
                                                 GUI.RADIUS + 1, Constants.GREEN)
                elif board[row][column] == Constants.COMPUTER:
                    pygame.gfxdraw.aacircle(GUI.screen, int(column * GUI.SLOT_SIZE + GUI.SLOT_SIZE / 2),
                                            GUI.height - int(row * GUI.SLOT_SIZE + GUI.SLOT_SIZE / 2), GUI.RADIUS + 1,
                                            Constants.ORANGE)
                    pygame.gfxdraw.filled_circle(GUI.screen, int(column * GUI.SLOT_SIZE + GUI.SLOT_SIZE / 2),
                                                 GUI.height - int(row * GUI.SLOT_SIZE + GUI.SLOT_SIZE / 2),
                                                 GUI.RADIUS + 1, Constants.ORANGE)
        pygame.display.update()

    @staticmethod
    def play(board):
        gameOver = False
        font = pygame.font.SysFont("arial", 50)
        turn = random.randint(Constants.PLAYER, Constants.COMPUTER)
        while not gameOver:
            # Computer turn
            if turn == Constants.COMPUTER and not gameOver:
                col, score = Minimax.minimax(board, Constants.DEPTH, -math.inf, math.inf, True)

                if GameService.isValidPosition(board, col):
                    row = GameService.getNextEmptyPositionOnColumn(board, col)
                    GameService.dropPiece(board, row, col, Constants.COMPUTER)

                    if GameService.isWinningMove(board, Constants.COMPUTER):
                        label = font.render("Computer wins!", 1, Constants.ORANGE)
                        GUI.screen.blit(label, (25, 10))
                        gameOver = True

                    if GameService.fullBoard(board):
                        label = font.render("Draw!", 1, Constants.ORANGE)
                        GUI.screen.blit(label, (25, 10))
                        gameOver = True
                    Utils.printBoard(board)
                    GUI.drawBoard(board)

                    turn = Constants.PLAYER
            else:
                # Ask for player input
                while turn == Constants.PLAYER and not gameOver:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == pygame.MOUSEMOTION:
                            pygame.draw.rect(GUI.screen, Constants.BLACK, (0, 0, GUI.width, GUI.SLOT_SIZE))
                            mousePositionX = event.pos[0]
                            pygame.gfxdraw.aacircle(GUI.screen, mousePositionX, int(GUI.SLOT_SIZE / 2), GUI.RADIUS,
                                                    Constants.GREEN)
                            pygame.gfxdraw.filled_circle(GUI.screen, mousePositionX, int(GUI.SLOT_SIZE / 2),
                                                         GUI.RADIUS - 7, Constants.GREEN)
                            pygame.display.update()

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pygame.draw.rect(GUI.screen, Constants.BLACK, (0, 0, GUI.width, GUI.SLOT_SIZE))
                            mousePositionX = event.pos[0]
                            col = int(math.floor(mousePositionX / GUI.SLOT_SIZE))

                            if GameService.isValidPosition(board, col):
                                row = GameService.getNextEmptyPositionOnColumn(board, col)
                                GameService.dropPiece(board, row, col, Constants.PLAYER)

                                if GameService.isWinningMove(board, Constants.PLAYER):
                                    label = font.render("Hurray, you won !", 1, Constants.ORANGE)
                                    GUI.screen.blit(label, (25, 10))
                                    gameOver = True

                                if GameService.fullBoard(board):
                                    label = font.render("Draw!", 1, Constants.ORANGE)
                                    GUI.screen.blit(label, (25, 10))
                                    gameOver = True

                                turn = Constants.COMPUTER

                                Utils.printBoard(board)
                                GUI.drawBoard(board)

        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
