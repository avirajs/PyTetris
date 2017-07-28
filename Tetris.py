# tetris.py
# Aviraj Sinha
# 9 hours
# pauses,reverses(z is counter clockwise,x is clockwise),hard drop,splash screen, levels

import random
from Tkinter import *


def keyPressed(event):
    # speeds
    if event.keysym == "1":
        cd.level = 1
    if event.keysym == "2":
        cd.level = 2
    if event.keysym == "3":
        cd.level = 3

    # moving/rotating
    if cd.gameover == False and cd.pause == False:
        if event.keysym == "Left":
            moveFallingPiece(0, -1)
        elif event.keysym == "Right":
            moveFallingPiece(0, 1)
        elif event.keysym == "Down":
            moveFallingPiece(1, 0)
        elif event.keysym == "Up" or event.keysym == "x":  # clckwise
            rotateFallingPiece()
        elif event.keysym == "z":
            reverse()
            if not (fallingPieceIsLegal()):  # cnt clckise
                rot()
    # restarts
    elif event.keysym == "r":
        init()
    if event.keysym == 'p':
        cd.pause = not cd.pause
    if event.keysym == "space":
        harddrop()

    redrawAll()


def harddrop():
    while moveFallingPiece(1, 0):
        None
    redrawAll()


def ifix():
    # ipiece mus be given a center
    if cd.piece == [(True, True, True, True)]:
        moveFallingPiece(0, -1)
        moveFallingPiece(1, 0)
    if cd.piece == [(True,), (True,), (True,), (True,)]:
        moveFallingPiece(0, 1)
        moveFallingPiece(-1, 0)


def reverse():
    # rot 3 brings it back
    rot()
    rot()
    rot()


def rot():
    # makes a backwards list then zips the cols to make the rotated piece
    rpiece = zip(*cd.piece[::-1])
    cd.piece = rpiece


def brotate():
    pass


def rotateFallingPiece():
    # rotates cntr cw
    rot()

    # moves piece back if illegal
    if not (fallingPieceIsLegal()):
        reverse()

    # keeps center
    ifix()


def moveFallingPiece(drow, dcol):
    rorig, corig = cd.rows, cd.cols
    cd.rows += drow
    cd.cols += dcol

    # moves piece back if illegal
    if not (fallingPieceIsLegal()):
        cd.rows -= drow
        cd.cols -= dcol

    # checks whether piece can move
    if rorig == cd.rows and corig == cd.cols:
        return False
    return True


def fallingPieceIsLegal():
    for r in xrange(len(cd.piece)):
        for c in xrange(len(cd.piece[r])):
            if cd.piece[r][c] == True:

                # checks if piece in in board
                if r + cd.rows < 0 or c + cd.cols < 0 or r + cd.rows > cd.nrows - 1 or c + cd.cols > cd.ncols - 1:
                    return False

                # checks if position is empty
                if board[r + cd.rows][c + cd.cols] != cd.empty:
                    return False

    return True


def newFallingPiece():
    # sets up random piece
    cd.piece = random.choice(cd.tetrisPieces)
    cd.color = random.choice(cd.tetrisPieceColors)
    cd.cols = 0
    cd.rows = 0

    # sets up middle for each piece
    cd.cols += cd.ncols / 2 - len(cd.piece[0]) / 2
    redrawAll()


def timerFired():
    if cd.pause == True:
        paused()
    else:
        redrawAll()

        # keeps playing the game unless the last piece that pops up is illegal
        if not fallingPieceIsLegal():
            cd.gameover = True

        # every time the piece cannot move
        if moveFallingPiece(+1, 0) == False:
            placeFallingPiece()
            # add a new piece
            newFallingPiece()

        # adds score to a string
        cd.score = int(cd.score)
        cd.score += len(findFullRow()) ** 2

        # remove full rows
        removeFullRows()

    delay = 900 - cd.level * 250
    canvas.after(delay, timerFired)


def paused():
    cd.score = str(cd.score)
    canvas.create_text(125, 150, text="\t   Game Paused! \n\t   Press p again to continue\n\t   Score: " + cd.score,
                       fill="lightblue", font="Castellar 13")


def placeFallingPiece():
    # makes piece part of the board
    for r in xrange(len(cd.piece)):
        for c in xrange(len(cd.piece[r])):
            if cd.piece[r][c] == True:
                board[r + cd.rows][c + cd.cols] = cd.color


def findFullRow():
    # start from the bottom putting full rows in list
    r = cd.nrows - 1
    iffull = True
    rows = []
    while r > 0:
        iffull = True
        for c in board[r]:
            if c == cd.empty:
                iffull = False
        if iffull == True:
            rows.append(r)
        r -= 1

    return rows


def removeFullRows():
    # clear full rows from the top
    for r in findFullRow():
        i = r
        while i > 0:
            board[i] = board[i - 1]
            i -= 1


def redrawAll():
    # makes each view of the board

    if cd.gameover == False:

        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, cd.canvasWidth, cd.canvasHeight, fill="orange", outline="orange")
        cd.score = str(cd.score)
        canvas.create_text(cd.canvasWidth / 2, 15, text="Tetris", font="Castellar 25")
        canvas.create_text(60, 12, text=" Score: " + str(cd.score) + " Level: " + str(cd.level), font="Castellar 10")
        drawboard()
        drawFallingPiece()
    else:

        # output once game is over
        cd.score = str(cd.score)
        canvas.create_text(125, 150, text="\t  Game Over! \n\t  Press r to Restart\n\t  Score: " + cd.score,
                           fill="Green", font="Castellar 16")


def drawboard():
    for r in xrange(cd.nrows):
        for c in xrange(cd.ncols):
            drawCell(r, c, board[r][c])


def drawFallingPiece():
    for r in xrange(len(cd.piece)):
        for c in xrange(len(cd.piece[r])):
            if cd.piece[r][c] == True:
                drawCell(r + cd.rows, c + cd.cols, cd.color)


def drawCell(row, col, color):
    canvas.create_rectangle(cd.margin + cd.cellSize * col, cd.margin + cd.cellSize * row,
                            cd.margin + cd.cellSize * (col + 1), cd.margin + cd.cellSize * (row + 1), fill=color,
                            width=4, outline="gray")


def init():
    # your global variables
    global cd
    cd = canvas.data
    cd.empty = 'Blue'
    cd.gameover = False
    cd.pause = False
    cd.level = 1

    # these are in game should not be edited
    cd.rows = 0
    cd.cols = 0
    cd.score = 0
    cd.gameover = False

    global board
    board = []
    for r in xrange(cd.nrows):
        board += [[cd.empty] * cd.ncols]

    # Seven "standard" pieces (tetrominoes)

    iPiece = [[True, True, True, True]]

    jPiece = [[True, False, False], [True, True, True]]

    lPiece = [[False, False, True], [True, True, True]]

    oPiece = [[True, True], [True, True]]

    sPiece = [[False, True, True], [True, True, False]]

    tPiece = [[False, True, False], [True, True, True]]

    zPiece = [[True, True, False], [False, True, True]]

    # possible combinations
    cd.tetrisPieces = [iPiece, tPiece, zPiece, sPiece, oPiece, lPiece, jPiece]
    cd.tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", "green", "orange"]

    # initialize
    newFallingPiece()
    redrawAll()


########### copy-paste below here ###########

def run(rows=15, cols=10):
    # normal variables (changeable)

    nrows = rows
    ncols = cols
    margin = 40
    cellSize = 30
    canvasWidth = 2 * margin + cols * cellSize
    canvasHeight = 2 * margin + rows * cellSize

    # splash
    root = Tk()
    splash = Canvas(root, width=canvasWidth, height=canvasHeight)
    splash.pack()
    splash.create_rectangle(0, 0, canvasWidth, canvasHeight, fill="orange")
    root.resizable(width=0, height=0)  # makes window non-resizable
    splash.create_text(canvasWidth / 2, canvasHeight / 3, text="Tetris", font="Castellar 30")
    splash.create_text(canvasWidth / 2, canvasHeight * (2 / 3.), text="Aviraj Sinha", font="Castellar 15")
    splash.create_text(70, 10, text="Close to see instructions", font="Castellar 5")
    root.mainloop()

    # splash 2
    root = Tk()
    splash2 = Canvas(root, width=canvasWidth, height=canvasHeight)
    splash2.pack()
    splash2.create_rectangle(0, 0, canvasWidth, canvasHeight, fill="orange")
    root.resizable(width=0, height=0)  # makes window non-resizable
    splash2.create_text(canvasWidth / 2, canvasHeight * (1 / 10.), text="Instructions", font="Castellar 15")
    splash2.create_text(canvasWidth / 2, canvasHeight * (2 / 9.), text="Use Arrow Keys to move Piece",
                        font="Castellar 10")
    splash2.create_text(canvasWidth / 2, canvasHeight * (3 / 9.), text="Hard drop is spacebar", font="Castellar 10")
    splash2.create_text(canvasWidth / 2, canvasHeight * (4 / 9.), text="Pressing P pauses", font="Castellar 10")
    splash2.create_text(canvasWidth / 2, canvasHeight * (5 / 9.), text="Reverses:", font="Castellar 10")
    splash2.create_text(canvasWidth / 2, canvasHeight * (6 / 9.), text="z is counter clockwise,x is clockwise",
                        font="Castellar 10")
    splash2.create_text(canvasWidth / 2, canvasHeight * (7 / 9.), text="Press a key for a level 1-3 during game",
                        font="Castellar 10")
    splash2.create_text(canvasWidth / 2, canvasHeight * (8 / 9.), text="Close Window to Start", font="Castellar 10")
    root.mainloop()

    # create the root and the canvas
    global canvas
    root = Tk()
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0, height=0)  # makes window non-resizable

    # Set up canvas data and call init
    class Struct: pass

    canvas.data = Struct()
    cd = canvas.data
    cd.nrows = nrows
    cd.ncols = ncols
    cd.margin = margin
    cd.cellSize = cellSize
    cd.canvasWidth = canvasWidth
    cd.canvasHeight = canvasHeight
    cd.level = 1

    init()

    # set up events
    root.bind("<Key>", keyPressed)
    timerFired()

    # launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)


run(15, 10)  # adjustable

