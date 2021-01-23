class GameState():
    ''' Holds the game state, position of pieces on board,
        black or white move turn and previous moves in moveLog '''
    def __init__(self):                                                 # Init for starting board state, sorted by row and column (r, c).
        self.board = [
            #Col:0 Col:1 Col:2 Col:3 Col:4 Col:5 Col:6 Col:7
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], #---------> Row: 0
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], #---------> Row: 1
            ["--", "--", "--", "--", "--", "--", "--", "--"], #---------> Row: 2
            ["--", "--", "--", "--", "--", "--", "--", "--"], #---------> Row: 3
            ["--", "--", "--", "--", "--", "--", "--", "--"], #---------> Row: 4
            ["--", "--", "--", "--", "--", "--", "--", "--"], #---------> Row: 5
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"], #---------> Row: 6
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]] #---------> Row: 7
        self.whiteToMove = True                                         # Booleen switch between white and black moves.
        self.moveLog = []                                               # Holds a log of all moves, functions append.
        self.moveFunctions = {                                          # Dictionary of all move functions, so if statements are not too messy.
                "p":self.getPawnMoves, "R":self.getRookMoves,
                "N":self.getKnightMoves,"B":self.getBishopMoves,
                "Q":self.getQueenMoves, 'K':self.getKingMoves
                }

    def makeMove(self, move):
        ''' Takes in data from move and executes it.'''
        self.board[move.startRow][move.startCol] = "--"                 # Capture Piece will not work with castling or pawn promotion.
        self.board[move.endRow][move.endCol] = move.pieceMoved          # Move piece
        print(move.pieceMoved)                                          # Print where piece moved
        self.moveLog.append(move)                                       # Log move.
        self.whiteToMove = not self.whiteToMove                         # Flips bool when move is completed, changing turn

    def undoMove(self):
        ''' Z mapped to undo move also, changes move log and turn. '''
        if len(self.moveLog) != 0:                                      # Make sure this is not first turn, since we cannot undo anything that isn't moved.
            move = self.moveLog.pop()                                   # Remove last move from move log.
            self.board[move.startRow][move.startCol] = move.pieceMoved  # Move piece back.
            self.board[move.endRow][move.endCol] = move.pieceCaptured   # Uncapture piece if that is the case.
            self.whiteToMove = not self.whiteToMove                     # Change move turn.

    def getValidMoves(self):                                            # Get valid moves ignoring for now.
        return self.getAllPossibleMoves()                               # Return call to getAllPossibleMoves.

    def getAllPossibleMoves(self):
        ''' Get all possible moves for each piece
            Calls functions for each piece when
            iterating through the board with dict'''
        moves = []                                                      # Holds list of all possible moves
        for r in range(len(self.board)):                                # iterate through all rows
            for c in range(len(self.board[r])):                         # Iterate through all columns
                turn = self.board[r][c][0]                              # Indetify whose turn it is either white or block

                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove): # Check if either black or white to move
                    piece = self.board[r][c][1]                         # Get pieces through each iteration.
                    self.moveFunctions[piece](r, c, moves)              # Calling move functions from above dictionary with piece and passing it (r, c, moves).
        return moves                                                    # Returns all possible moves list.


    def getPawnMoves(self, r, c, moves):                                # Get all possible pawn moves appends these to possible moves list.
        ''' Get all Knight moves. '''
        if self.whiteToMove:    # * White to move. *

            if self.board[r-1][c] == "--":                              # Checking to make sure white's 1+ forward square is empty.
                moves.append(Move(                                      # Append to available moves list.
                    (r, c), (r-1, c), self.board))

                if r == 6 and self.board[r-2][c] == "--":               # Checking pawns are on starting squares and +2 forward square is empty.
                    moves.append(Move(                                  # Append to available moves list.
                        (r, c), (r-2, c), self.board))
                                                                        # Pawn right and left #
            if c-1 >= 0:                                                # Left limit insuring we do not go off board.
                if self.board[r-1][c-1][0] == "b":                      # Checking if black's enemy piece, is on a left diagonal to this piece.
                    moves.append(Move(                                  # Append to available moves list.
                        (r, c), (r-1, c-1), self.board))

            if c+1 <= 7:                                                # Right Limit
                if self.board[r-1][c+1][0] == "b":                      # Checking if black's enemy piece, is on a left diagonal to this piece.
                    moves.append(Move(                                  # Append to available moves list.
                        (r, c), (r-1, c+1), self.board))

        else:                                                           # * BLACK TO MOVE. *

            if self.board[r+1][c] == "--":                              # Checking to make sure black's 1+ forward square is empty.
                moves.append(Move(                                      # Append to available moves list.
                    (r, c), (r+1, c), self.board))

                if r==1 and self.board[r+2][c] == "--":                 # Checking pawns are on starting squares and +2 forward square is empty.
                    moves.append(Move(                                  # Append to available moves list.
                        (r, c), (r+2, c), self.board))

                                                                        # Pawn right and left #
            if c-1 >= 0:                                                # Right limit insuring we do not go off board
                if self.board[r+1][c-1][0] == "w":                      # If white enemy piece is on a right diagonal to this piece
                    moves.append(Move(                                  # Append to available moves list.
                        (r, c), (r+1, c-1), self.board))

            if c+1 <= 7:                                                # Left limit insuring we do not go off board
                if self.board[r+1][c+1][0] == "w":                      # If enemy piece is on a reft diagonal to this piece
                    moves.append(Move(                                  # Append to available moves list.
                        (r, c), (r+1, c+1), self.board))


    def getRookMoves(self, r, c, moves):
        ''' Get all Rook moves. '''
        rookDirections = (      # * White's perspective *
                (-1, 0),        # 1 : (left)
                (0, -1),        # 2 : (down)
                (1,  0),        # 3 : (right
                (0,  1))        # 4 : (up)
        enemyColor = "b" if self.whiteToMove else "w"                   # Setting enemy color, maybe we can find a better way? TODO
        print(f"ROOK: Location {r, c} enemcy color is {enemyColor}")    # Print statement for *DEBUGGING.*
        for d in rookDirections:
            print(d)                                                    # Print statement for *DEBUGGING.*
            for i in range(1, 8):                                       # Rook can move max of 7 squares.
                print(i)                                                # Print statement for *DEBUGGING.*
                endRow = r + d[0] * i                                   # Adds row to row direction and scales it by i, the Rook's movement range.
                endCol = c + d[1] * i                                   # Adds columnn to column direction and scales it by i, the Rook's movement range.
                print(endRow, endCol)                                   # Print statement for *DEBUGGING.*

                if 0 <= endRow < 8 and 0 <= endCol < 8:                 # Check to make sure we don't go "out of bounds" on board.
                    endPiece = self.board[endRow][endCol]               # Setting our endpiece to endRow and endCol
                    if endPiece == "--": # Empty Square.
                        moves.append(Move(
                            (r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move(
                            (r, c), (endRow, endCol), self.board))
                        break
                    else: # Friendly piece.
                        print("break friendly piece")
                        break
                else: # Off of board.
                    print("break off board")
                    break


    def getKnightMoves(self, r, c, moves):
        ''' Get all Knight moves. '''
        knightDirections = (    # * White's perspective *
                (-2, -1),       # 1
                (-2,  1),       # 2
                (-1, -2),       # 3
                (-1,  2),       # 4
                (1,  -2),       # 5
                (1,   2),       # 6
                (2,  -1),       # 7
                (2,   1))       # 8
        allyColor = "w" if self.whiteToMove else "b"
        print(f"KNIGHT: Location {r, c} ally color is {allyColor}")
        for m in knightDirections:
            endRow = r + m[0]
            endCol = c + m[1]
            print(f"End row and col: {endRow, endCol}")

            if 0 <= endRow < 8 and 0 <= endCol < 8: # Checking if on board
                endPiece = self.board[endRow][endCol]
                print(f"Hello endpiece!: {endPiece}")
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        ''' Get all Bishop moves. '''

        bishopDirections = (    # *White's Perspective*
                (-1, -1),       # 1 : (left, up)
                (-1,  1),       # 2 : (left, down)
                (1,  -1),       # 3 : (right, up)
                (1,   1))       # 4 : (right, down)
        enemyColor = "b" if self.whiteToMove else "w"
        print(f"BISHOP: Location {r, c} enemcy color is {enemyColor}")

        for d in bishopDirections:
            print(d)
            for i in range(1, 8): # Bishop can move max of 7 squares
                print(i)
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                print(endRow, endCol)

                if 0 <= endRow < 8 and 0 <= endCol < 8: # Checking we're on the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # Empty space valid
                        moves.append(Move(
                            (r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # Enemy piece valid move
                        moves.append(Move(
                            (r, c), (endRow, endCol), self.board))
                        break
                    else: # Friendly piece not a valid move.
                        print("Break friendly piece")
                        break
                else: # Off board.
                    print("Break off board")
                    break


    def getQueenMoves(self, r, c, moves):
        ''' Get all Queen moves. '''
        self.getRookMoves(r, c, moves)                          # Since the queen is essentially just a rook and a bishop, we can just call those functions.
        self.getBishopMoves(r, c, moves)


    def getKingMoves(self, r, c, moves):
        ''' Get all King moves. '''
        kingMoves = (
                (-1, -1),
                (-1,  0),
                (-1,  1),
                (0,  -1),
                (0,   1),
                (1,  -1),
                (1,   0),
                (1,   1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move(
                        (r, c), (endRow, endCol), self.board))





class Move():
            ### Change to chess notation ###
    ranksToRows = { "1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0 }

    filesToCols = { "a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7 }

    rowsToRanks = {v: k for k, v in ranksToRows.items()}        # Changes rows to ranks based on dictionary above.
    colsToFiles = {v: k for k, v in filesToCols.items()}        # Changes cols to files based on dictionary above.


    def __init__(self, startSq, endSq, board):
        # Constructor
        self.startRow = startSq[0]
        self.startCol = startSq[1]

        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol # Unique move ID for each move
        print(f"Move ID: {self.moveID}")


    # Overriding equals method
    def __eq__(self, other):
        if isinstance(other, Move): # Overriding equals methd
            return self.moveID == other.moveID # comparing move ID
            if self.moveID == other.moveID:
                print("EQ: Equal")
        else:
            return False # Return false if no equality.
            print("EQ: NOT Equal")




    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    ### Converts row and collumn data to rank and file data from rows to colls above dict ###
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
