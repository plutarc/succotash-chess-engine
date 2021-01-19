
class GameState():
    ''' Holds the game state, position of pieces on board, 
        black or white move turn and previous moves in moveLog '''
    def __init__(self):
        self.board = [
            #Col:0 Col:1 Col:2 Col:3 Col:4 Col:5 Col:6 Col:7
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], # Row:0 
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], # Row:1 
            ["--", "--", "--", "--", "--", "--", "--", "--"], # Row:2 
            ["--", "--", "--", "--", "--", "--", "--", "--"], # Row:3 
            ["--", "--", "--", "--", "--", "--", "--", "--"], # Row:4 
            ["--", "--", "--", "--", "--", "--", "--", "--"], # Row:5 
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"], # Row:6 
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]] # Row:7 
        self.whiteToMove = True # Booleen switch for move
        self.moveLog = [] # Holds all moves functions append

        self.moveFunctions = {"p":self.getPawnMoves, "R":self.getRookMoves, "N":self.getKnightMoves, 
                              "B":self.getBishopMoves, "Q":self.getQueenMoves, 'K':self.getKingMoves}

    def makeMove(self, move):
	''' Takes in data from move and executes it.'''
        self.board[move.startRow][move.startCol] = "--" # Capture Piece will not work with castling or pawn promotion. 
        self.board[move.endRow][move.endCol] = move.pieceMoved # Move piece  
        print(move.pieceMoved) # Print where piece moved
        self.moveLog.append(move) # Log the move 
        self.whiteToMove = not self.whiteToMove # Change move turn 

    def undoMove(self):
	''' Z mapped to undo move also, changes move log and turn. '''
        if len(self.moveLog) != 0: # Make sure this is not first turn, since we cannot undo anything that isn't moved  
            move = self.moveLog.pop() # Remove last move from move log 
            self.board[move.startRow][move.startCol] = move.pieceMoved # Move piece back 
            self.board[move.endRow][move.endCol] = move.pieceCaptured # Uncapture piece if that is the case 
            self.whiteToMove = not self.whiteToMove # Change move turn. 

    ### Get's Valid moves after getting possible moves. ###
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    ### Get's all possible moves for each piece ### 
    def getAllPossibleMoves(self):
        moves = [] # Holds list of all possible moves
        for r in range(len(self.board)): # iterate through all rows
            for c in range(len(self.board[r])): # Iterate through all columns  
                turn = self.board[r][c][0] # Indetify whose turn it is either white or block

                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove): # Check if either black or white to move  
                    piece = self.board[r][c][1] # Get pieces through each iteration. 
                    self.moveFunctions[piece](r, c, moves)
        return moves

    ### Get all pawn moves for row col and add these moves to the list ###

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # White to move
            if self.board[r-1][c] == "--": # Check one square in front. 
                moves.append(Move((r, c), (r-1, c), self.board)) # Append move. 
                if r == 6 and self.board[r-2][c] == "--": # 2 Square pawn advance Check if white is on Row 6 and 2 squares in front is clear.
                    moves.append(Move((r, c), (r-2, c), self.board))

            # Pawn right and left captures #
            if c-1 >= 0: # Left Limit  
                if self.board[r-1][c-1][0] == "b": # if enemy piece to the left diagonal. 
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: # Right Limit
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board)) # If enemy piece to right diagonal. 

        else: # Black to move.
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r==1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))

            # Pawn right and left captures #
            if c-1 >= 0: # Right Limit
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7: # Left Limit
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))


    def getRookMoves(self, r, c, moves):
        pass
    
    def getKnightMoves(self, r, c, moves):
        pass

    def getBishopMoves(self, r, c, moves):
        pass
    
    def getQueenMoves(self, r, c, moves):
        pass

    def getKingMoves(self, r, c, moves):
        pass
    
                        




class Move():
            ### Change to chess notation ###
    ranksToRows = { "1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0 } 

    filesToCols = { "a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7 }

    rowsToRanks = {v: k for k, v in ranksToRows.items()} # Changes rows to ranks based on dictionary above.  
    colsToFiles = {v: k for k, v in filesToCols.items()} # Changes cols to files based on dictionary above. 


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
