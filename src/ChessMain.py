import pygame as p
import ChessEngine


WIDTH = HEIGHT = 512
DIMENSION = 8 # Defining 8x8 Chess Board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # Global refresh rate

IMAGES = {}                                                     # Intitalizing Dict to hold loaded images.

def loadImages():
    """ Run only once but loads images into IMAGES global Dict. """

    pieces = ["bB", "bK", "bN", 'bp', "bQ", "bR",               # List of image names in src folder. 
              "wB", "wK", "wN", "wp", "wQ", "wR"]
    for piece in pieces:                                        # Looping and loading image list on startup
        IMAGES[piece] = p.transform.scale(p.image.load(         # Get correct sizing for images. 
            f"chess_images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def main():
    """ Main logic for Game """

    p.init()                                                    # Initialize for pygame

    screen = p.display.set_mode((WIDTH, HEIGHT))                # Set Screen size for Pygame
    clock = p.time.Clock()                                      # Init Clock for timing.
    screen.fill(p.Color("White"))                               # Temporary Screen fill white

    gs = ChessEngine.GameState()                                # Initialize Game State Object.
    validMoves = gs.getValidMoves()                             # Gets a list of valid moves from game state.
    moveMade = False                                            # Flag variable for when a move is made by either white or black.
    loadImages()                                                # Loads images once upon starting.
    mouseClicks = 0                                             # Holds mouse clicks for debuging UI.

    sqSelected = ()                                             # Tuple holds current square selected by (row, col)
    playerClicks = []                                           # Holds two tuples [(0, 1), (2, 1)], first tuple is the first player click from starting location secon                                                                 # d tuple is where player wishes to move. holds two values of sqSelected

    running = True # Running flag if set to false game quits.


    print('Initializing Main Loop')
    while running:                                              # Main init. CLEAN ALL OF THIS UP! TODO

        for e in p.event.get():

            if e.type == p.QUIT:                                # IF* we see a keypress quit change While loop to false.
                running = False                 #                SET* While LOOP value to False which will quit the program.

                                                                # Mouse Handler
            elif e.type == p.MOUSEBUTTONDOWN:                   # Check for click
                location = p.mouse.get_pos()                    # x y Location of the mouse

                if mouseClicks % 2 == 0 and mouseClicks != 1:
                    print("\n")
                    print(f"LOGIC SEQUENCE {mouseClicks*0.5}")
                mouseClicks += 1

                if mouseClicks % 2 != 0:
                    print("FIRST CLICK")

                if mouseClicks % 2 == 0:
                    print("SECOND ClICK")

                col = location[0]//SQ_SIZE                      # Get Column where clicked when the mouse is pressed dividing by scare size for accuracy.
                row = location[1]//SQ_SIZE                      # Get Row where clicked when the mouse is pressed divivding by square size for accuracy.

                if sqSelected == (row, col):                    # User clicked the same square twice. Clear both sqSelected and playerClicks
                    print(f"    CHECK: FAIL! User *DID* click the same square twice at: {sqSelected}")
                    print(f"        CHECK: FAIL!: SELECTED SAME SQUARE TWICE! sqSelected & playerClicks after at: {playerClicks}")
                    sqSelected = ()                             # Clear ALL
                    playerClicks = []                           # Clear ALL
                    print("*CLEARED!*")                         # Printing that both have been cleared

                else:                                           # If user did not click same square twice find square selected and add to playerClicks
                    sqSelected = (row, col)                     # Square selected add row and column of player clicks
                    print(f"    CHECK!: OK! User did *NOT* click the same square twice at: {sqSelected}")
                    playerClicks.append(sqSelected)             # Append above square selected to player clicks
                    print(f"        CHECK!: OK! sqSelected appeneded to playerClicks: {playerClicks}")

                if len(playerClicks) == 2:                      # Make sure the playerClicks size is 2 so that we know it is row and col and not any extra garbage
                    print("             CHECK!: OK!: 2 clicks!")
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board) # Call move function from chess engine unpack playerClicks tuple and calls board
                    print(f"Chess Notation: {move.getChessNotation()}")
                    print(f"MOVE: {move}")


                    if move in validMoves:                      # IF* we have a valid move check before making an actual move.
                        print(f"    CHECK!: OK!: MOVE from: {playerClicks[0]} to: {playerClicks[1]} *VALID*: \n")
                        gs.makeMove(move)                       # Makes move passed move object
                        moveMade = True                         # Move made flag to True, so we can call getValidMoves Below without calling every frame.
                        sqSelected = ()                         # After *MOVE* clear *ALL*
                        playerClicks = []                       # After *MOVE* clear *ALL*

                    else:
                        print(f"    CHECK!: FAIL!: MOVE from: {playerClicks[0]} to: {playerClicks[1]} *NOT VALID*: \n")
                        playerClicks = [sqSelected]             # Not sure why this works. TODO

                    print(f'CHECK!: OK: sqSelected & playerClicks after {playerClicks}')
                    print("*CLEARED!*")                         # Printing that both have been cleared

                else:
                    print("            CHECK!: FAIL! not unique 2 clicks")

            elif e.type == p.KEYDOWN:                           # Check for keypress
                if e.key == p.K_z:                              # IF* keypress is "Z" Undo move
                    gs.undoMove()                               # Call Undo Move
                    moveMade = True                             # Reset move made flag to recheck valid moves

        if moveMade:                                            # When move is made do below
            validMoves = gs.getValidMoves()                     # Only generate valid moves when a move is made.
            moveMade = False                                    # Setting move state flag back to false
            print('***MOVE MADE***')

        drawGameState(screen, gs)                               # Calls two functions to draw board and pieces
        clock.tick(MAX_FPS)                                     # What? TODO
        p.display.flip()                                        # No idea WHAT? TODO


def drawGameState(screen, gs):
    """ Draw board and draw pieces so that we can
    draw pieces and board seperately. """

    drawBoard(screen)
    drawPieces(screen, gs.board)



def drawBoard(screen):
    """ Draws board """

    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



def drawPieces(screen, board):
    """ Draws pieces. """

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))


if __name__ == "__main__":
    main()
