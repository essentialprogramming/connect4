from utils.Utils import Utils
from ui.Gui import GUI


def start():
    board = Utils.createBoard()
    Utils.printBoard(board)

    GUI.drawBoard(board)
    GUI.play(board)
    # UI.play(board)


start()
