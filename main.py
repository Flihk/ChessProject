# importing
import pygame


# class for board and actually playing
class Board(object):
    def __init__(self):
        # pieces (it's a lot)
        # white pieces
        self.whiteList = []
        for i in range(0, 8):
            self.whiteList.append(Pawn("White", i, 6))
        self.whiteList.append(Rook("White", 0, 7))
        self.whiteList.append(Knight("White", 1, 7))
        self.whiteList.append(Bishop("White", 2, 7))
        self.whiteList.append(Queen("White", 3, 7))
        self.whiteList.append(King("White", 4, 7))
        self.whiteList.append(Bishop("White", 5, 7))
        self.whiteList.append(Knight("White", 6, 7))
        self.whiteList.append(Rook("White", 7, 7))

        # black pieces
        self.blackList = []
        for i in range(0, 8):
            self.blackList.append(Pawn("Black", i, 1))
        self.blackList.append(Rook("Black", 0, 0))
        self.blackList.append(Knight("Black", 1, 0))
        self.blackList.append(Bishop("Black", 2, 0))
        self.blackList.append(Queen("Black", 3, 0))
        self.blackList.append(King("Black", 4, 0))
        self.blackList.append(Bishop("Black", 5, 0))
        self.blackList.append(Knight("Black", 6, 0))
        self.blackList.append(Rook("Black", 7, 0))

        # start the board
        self.update()

    def update(self):
        self.board = [["_", "_", "_", "_", "_", "_", "_", "_"],
                      ["_", "_", "_", "_", "_", "_", "_", "_"],
                      ["_", "_", "_", "_", "_", "_", "_", "_"],
                      ["_", "_", "_", "_", "_", "_", "_", "_"],
                      ["_", "_", "_", "_", "_", "_", "_", "_"],
                      ["_", "_", "_", "_", "_", "_", "_", "_"],
                      ["_", "_", "_", "_", "_", "_", "_", "_"],
                      ["_", "_", "_", "_", "_", "_", "_", "_"]]

        # putting pieces on board
        for piece in self.whiteList:
            self.board[piece.row][piece.col] = piece.notate
        for piece in self.blackList:
            self.board[piece.row][piece.col] = piece.notate

    def query(self):
        self.update()
        print("\n")
        for i in range(0, 8):
            print(self.board[i])


# parent class for all piece classes
class Piece(object):
    def __init__(self, color, col, row):
        self.color = color
        self.col = col
        self.row = row
        self.col2 = col
        self.row2 = col
        self.returnList = []
        self.moveList = []
        self.whileVar = 1

    def Move(self, col, row):
        if inList(self.PossibleMoves(), [col, row]):
            self.col = col
            self.row = row
            if(main.board[row][col] != "_"):
                if(self.color == "White"):
                    for i in main.blackList:
                        if(i.col == self.col and i.row == self.row):
                            i.Captured()
                else:
                    for i in main.whiteList:
                        if (i.col == self.col and i.row == self.row):
                            i.Captured()

            main.query()
        else:
            print("Invalid Move")

    def Captured(self):
        if (self.color == "White"):
            main.whiteList.remove(self)
        else:
            main.blackList.remove(self)


# king class
class King(Piece):
    def __init__(self, color, col, row):
        super().__init__(color, col, row)
        if (color == "White"):
            self.notate = "K"
        else:
            self.notate = "k"

    def PossibleMoves(self):
        self.returnList = [[self.col-1, self.row-1], [self.col-0, self.row-1], [self.col+1, self.row-1],
                           [self.col-1, self.row-0],                       [self.col+1, self.row-0],
                           [self.col-1, self.row+1], [self.col-0, self.row+1], [self.col+1, self.row+1]]
        # removing invalid diagonal moves
        if (self.col == 0 or self.row == 0):
            self.returnList.remove([self.col-1, self.row-1])
        if (self.col == 7 or self.row == 0):
            self.returnList.remove([self.col+1, self.row-1])
        if (self.col == 0 or self.row == 7):
            self.returnList.remove([self.col-1, self.row+1])
        if (self.col == 7 or self.row == 7):
            self.returnList.remove([self.col+1, self.row+1])
        # removing invalid cardinal moves
        if (self.col == 0):
            self.returnList.remove([self.col-1, self.row-0])
        if (self.col == 7):
            self.returnList.remove([self.col+1, self.row-0])
        if (self.row == 0):
            self.returnList.remove([self.col-0, self.row-1])
        if (self.row == 7):
            self.returnList.remove([self.col-0, self.row+1])
        return self.returnList


# queen class
class Queen(Piece):
    def __init__(self, color, col, row):
        super().__init__(color, col, row)
        if (color == "White"):
            self.notate = "Q"
        else:
            self.notate = "q"

    def PossibleMoves(self):
        self.returnList = []
        # vertical & horizontal movement
        # going left
        self.whileVar = 1
        while (self.col - self.whileVar >= 0 and main.board[self.row][self.col - self.whileVar] == "_"):
            self.returnList.append([self.col - self.whileVar, self.row])
            self.whileVar += 1
        if (self.col - self.whileVar >= 0):
            if (main.board[self.row][self.col - self.whileVar] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row and i.col == self.col - self.whileVar):
                            self.returnList.append([self.col - self.whileVar, self.row])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row and i.col == self.col - self.whileVar):
                            self.returnList.append([self.col - self.whileVar, self.row])
        # going right
        self.whileVar = 1
        while (self.col + self.whileVar <= 7 and main.board[self.row][self.col + self.whileVar] == "_"):
            self.returnList.append([self.col + self.whileVar, self.row])
            self.whileVar += 1
        if (self.col + self.whileVar <= 7):
            if (main.board[self.row][self.col + self.whileVar] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row and i.col == self.col + self.whileVar):
                            self.returnList.append([self.col + self.whileVar, self.row])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row and i.col == self.col + self.whileVar):
                            self.returnList.append([self.col + self.whileVar, self.row])
        # going up
        self.whileVar = 1
        while (self.row - self.whileVar >= 0 and main.board[self.row - self.whileVar][self.col] == "_"):
            self.returnList.append([self.col, self.row - self.whileVar])
            self.whileVar += 1
        if (self.row - self.whileVar >= 0):
            if (main.board[self.row - self.whileVar][self.col] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row - self.whileVar and i.col == self.col):
                            self.returnList.append([self.col, self.row - self.whileVar])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row - self.whileVar and i.col == self.col):
                            self.returnList.append([self.col, self.row - self.whileVar])
        # going down
        self.whileVar = 1
        while (self.row + self.whileVar <= 7 and main.board[self.row + self.whileVar][self.col] == "_"):
            self.returnList.append([self.col, self.row + self.whileVar])
            self.whileVar += 1
        if (self.row + self.whileVar <= 7):
            if (main.board[self.row + self.whileVar][self.col] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row + self.whileVar and i.col == self.col):
                            self.returnList.append([self.col, self.row + self.whileVar])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row + self.whileVar and i.col == self.col):
                            self.returnList.append([self.col, self.row + self.whileVar])

        # diagonal movement
        self.whileVar = 1
        while (self.row - self.whileVar >= 0 and self.col - self.whileVar >= 0 and (main.board[self.row - self.whileVar][self.col - self.whileVar] == "_")):
            self.returnList.append([self.col - self.whileVar, self.row - self.whileVar])
            self.whileVar += 1
        if (self.row - self.whileVar >= 0 and self.col - self.whileVar >= 0):
            if (main.board[self.row - self.whileVar][self.col - self.whileVar] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row - self.whileVar and i.col == self.col - self.whileVar):
                            self.returnList.append([self.col - self.whileVar, self.row - self.whileVar])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row - self.whileVar and i.col == self.col - self.whileVar):
                            self.returnList.append([self.col - self.whileVar, self.row - self.whileVar])
        # diagonal to top right
        self.whileVar = 1
        while (self.row - self.whileVar >= 0 and self.col + self.whileVar <= 7 and (main.board[self.row - self.whileVar][self.col + self.whileVar] == "_")):
            self.returnList.append([self.col + self.whileVar, self.row - self.whileVar])
            self.whileVar += 1
        if (self.row - self.whileVar >= 0 and self.col + self.whileVar <= 7):
            if (main.board[self.row - self.whileVar][self.col + self.whileVar] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row - self.whileVar and i.col == self.col + self.whileVar):
                            self.returnList.append([self.col + self.whileVar, self.row - self.whileVar])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row - self.whileVar and i.col == self.col + self.whileVar):
                            self.returnList.append([self.col + self.whileVar, self.row - self.whileVar])
        # diagonal to bottom left
        self.whileVar = 1
        while (self.row + self.whileVar <= 7 and self.col - self.whileVar >= 0 and (main.board[self.row + self.whileVar][self.col - self.whileVar] == "_")):
            self.returnList.append([self.col - self.whileVar, self.row + self.whileVar])
            self.whileVar += 1
        if (self.row + self.whileVar <= 7 and self.col - self.whileVar >= 0):
            if (main.board[self.row + self.whileVar][self.col - self.whileVar] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row + self.whileVar and i.col == self.col - self.whileVar):
                            self.returnList.append([self.col - self.whileVar, self.row + self.whileVar])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row + self.whileVar and i.col == self.col - self.whileVar):
                            self.returnList.append([self.col - self.whileVar, self.row + self.whileVar])
        # diagonal to bottom right
        self.whileVar = 1
        while (self.row + self.whileVar <= 7 and self.col + self.whileVar <= 7 and (main.board[self.row + self.whileVar][self.col + self.whileVar] == "_")):
            self.returnList.append([self.col + self.whileVar, self.row + self.whileVar])
            self.whileVar += 1
        if (self.row + self.whileVar <= 7 and self.col + self.whileVar <= 7):
            if (main.board[self.row + self.whileVar][self.col + self.whileVar] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row + self.whileVar and i.col == self.col + self.whileVar):
                            self.returnList.append([self.col + self.whileVar, self.row + self.whileVar])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row + self.whileVar and i.col == self.col + self.whileVar):
                            self.returnList.append([self.col + self.whileVar, self.row + self.whileVar])
        return self.returnList


# rook class
class Rook(Piece):
    def __init__(self, color, col, row):
        super().__init__(color, col, row)
        if (color == "White"):
            self.notate = "R"
        else:
            self.notate = "r"

    def PossibleMoves(self):
        self.returnList = []
        # going left
        self.whileVar = 1
        while (self.col - self.whileVar >= 0 and main.board[self.row][self.col - self.whileVar] == "_"):
            self.returnList.append([self.col - self.whileVar, self.row])
            self.whileVar += 1
        if (self.col - self.whileVar >= 0):
            if (main.board[self.row][self.col - self.whileVar] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row and i.col == self.col - self.whileVar):
                            self.returnList.append([self.col - self.whileVar, self.row])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row and i.col == self.col - self.whileVar):
                            self.returnList.append([self.col - self.whileVar, self.row])

        # going right
        self.whileVar = 1
        while (self.col + self.whileVar <= 7 and main.board[self.row][self.col + self.whileVar] == "_"):
            self.returnList.append([self.col + self.whileVar, self.row])
            self.whileVar += 1
        if (self.col + self.whileVar <= 7):
            if (main.board[self.row][self.col + self.whileVar] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row and i.col == self.col + self.whileVar):
                            self.returnList.append([self.col + self.whileVar, self.row])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row and i.col == self.col + self.whileVar):
                            self.returnList.append([self.col + self.whileVar, self.row])
        # going up
        self.whileVar = 1
        while (self.row - self.whileVar >= 0 and main.board[self.row - self.whileVar][self.col] == "_"):
            self.returnList.append([self.col, self.row - self.whileVar])
            self.whileVar += 1
        if (self.row - self.whileVar >= 0):
            if (main.board[self.row - self.whileVar][self.col] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row - self.whileVar and i.col == self.col):
                            self.returnList.append([self.col, self.row - self.whileVar])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row - self.whileVar and i.col == self.col):
                            self.returnList.append([self.col, self.row - self.whileVar])
        # going down
        self.whileVar = 1
        while (self.row + self.whileVar <= 7 and main.board[self.row + self.whileVar][self.col] == "_"):
            self.returnList.append([self.col, self.row + self.whileVar])
            self.whileVar += 1
        if (self.row + self.whileVar <= 7):
            if (main.board[self.row + self.whileVar][self.col] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row + self.whileVar and i.col == self.col):
                            self.returnList.append([self.col, self.row + self.whileVar])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row + self.whileVar and i.col == self.col):
                            self.returnList.append([self.col, self.row + self.whileVar])
        return self.returnList


# knight class
class Knight(Piece):
    def __init__(self, color, col, row):
        super().__init__(color, col, row)
        if (color == "White"):
            self.notate = "N"
        else:
            self.notate = "n"

    def PossibleMoves(self):
        # reset returnList
        self.returnList = []
        # up left movements
        if (self.col > 1 and self.row > 0):
            self.returnList.append([self.col-2, self.row-1])
        if (self.col > 0 and self.row > 1):
            self.returnList.append([self.col-1, self.row-2])
        # up right movements
        if (self.col < 6 and self.row > 0):
            self.returnList.append([self.col+2, self.row-1])
        if (self.col < 7 and self.row > 1):
            self.returnList.append([self.col+1, self.row-2])
        # down left movements
        if (self.col > 1 and self.row < 7):
            self.returnList.append([self.col-2, self.row+1])
        if (self.col > 0 and self.row < 6):
            self.returnList.append([self.col-1, self.row+2])
        # down right movements
        if (self.col < 6 and self.row < 7):
            self.returnList.append([self.col+2, self.row+1])
        if (self.col < 7 and self.row < 6):
            self.returnList.append([self.col+1, self.row+2])
        for i in self.returnList:
            if main.board[i[1]][i[0]] != "_":
                if self.color == "Black":
                    for k in main.blackList:
                        if (k.row == i[1] and k.col == i[0]):
                            self.returnList.remove(i)
                if self.color == "White":
                    for k in main.whiteList:
                        if (k.row == i[1] and k.col == i[0]):
                            self.returnList.remove(i)

        return self.returnList


# bishop class
class Bishop(Piece):
    def __init__(self, color, col, row):
        super().__init__(color, col, row)
        if (color == "White"):
            self.notate = "B"
        else:
            self.notate = "b"

    def PossibleMoves(self):
        self.returnList = []
        # diagonal to top left
        self.whileVar = 1
        while (self.row - self.whileVar >= 0 and self.col - self.whileVar >= 0 and (main.board[self.row - self.whileVar][self.col - self.whileVar] == "_")):
            self.returnList.append([self.col - self.whileVar, self.row - self.whileVar])
            self.whileVar += 1
        if (self.row - self.whileVar >= 0 and self.col - self.whileVar >= 0):
            if (main.board[self.row - self.whileVar][self.col - self.whileVar] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row - self.whileVar and i.col == self.col - self.whileVar):
                            self.returnList.append([self.col - self.whileVar, self.row - self.whileVar])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row - self.whileVar and i.col == self.col - self.whileVar):
                            self.returnList.append([self.col - self.whileVar, self.row - self.whileVar])
        # diagonal to top right
        self.whileVar = 1
        while (self.row - self.whileVar >= 0 and self.col + self.whileVar <= 7 and (main.board[self.row - self.whileVar][self.col + self.whileVar] == "_")):
            self.returnList.append([self.col + self.whileVar, self.row - self.whileVar])
            self.whileVar += 1
        if (self.row - self.whileVar >= 0 and self.col + self.whileVar <= 7):
            if (main.board[self.row - self.whileVar][self.col + self.whileVar] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row - self.whileVar and i.col == self.col + self.whileVar):
                            self.returnList.append([self.col + self.whileVar, self.row - self.whileVar])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row - self.whileVar and i.col == self.col + self.whileVar):
                            self.returnList.append([self.col + self.whileVar, self.row - self.whileVar])
        # diagonal to bottom left
        self.whileVar = 1
        while (self.row + self.whileVar <= 7 and self.col - self.whileVar >= 0 and (main.board[self.row + self.whileVar][self.col - self.whileVar] == "_")):
            self.returnList.append([self.col - self.whileVar, self.row + self.whileVar])
            self.whileVar += 1
        if (self.row + self.whileVar <= 7 and self.col - self.whileVar >= 0):
            if (main.board[self.row + self.whileVar][self.col - self.whileVar] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row + self.whileVar and i.col == self.col - self.whileVar):
                            self.returnList.append([self.col - self.whileVar, self.row + self.whileVar])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row + self.whileVar and i.col == self.col - self.whileVar):
                            self.returnList.append([self.col - self.whileVar, self.row + self.whileVar])
        # diagonal to bottom right
        self.whileVar = 1
        while (self.row + self.whileVar <= 7 and self.col + self.whileVar <= 7 and (main.board[self.row + self.whileVar][self.col + self.whileVar] == "_")):
            self.returnList.append([self.col + self.whileVar, self.row + self.whileVar])
            self.whileVar += 1
        if (self.row + self.whileVar <= 7 and self.col + self.whileVar <= 7):
            if (main.board[self.row + self.whileVar][self.col + self.whileVar] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.row == self.row + self.whileVar and i.col == self.col + self.whileVar):
                            self.returnList.append([self.col + self.whileVar, self.row + self.whileVar])
                else:
                    for i in main.whiteList:
                        if (i.row == self.row + self.whileVar and i.col == self.col + self.whileVar):
                            self.returnList.append([self.col + self.whileVar, self.row + self.whileVar])
        return self.returnList


# pawn class
class Pawn(Piece):
    def __init__(self, color, col, row):
        super().__init__(color, col, row)
        if (color == "White"):
            self.notate = "P"
        else:
            self.notate = "p"
        self.hasMoved = False

    def PossibleMoves(self):
        self.returnList = []
        if self.color == "White":
            self.returnList = [                      [self.col, self.row-2],
                               [self.col-1, self.row-1], [self.col, self.row-1], [self.col+1, self.row-1]]
            if main.board[self.row-1][self.col] != "_":
                self.returnList.remove([self.col, self.row-1])
                self.returnList.remove([self.col, self.row-2])
            elif main.board[self.row-2][self.col] != "_":
                self.returnList.remove([self.col, self.row-2])
            elif self.hasMoved:
                self.returnList.remove([self.col, self.row-2])
            if self.col == 0:
                self.returnList.remove([self.col-1, self.row-1])
            elif main.board[self.row-1][self.col-1] == "_":
                self.returnList.remove([self.col-1, self.row-1])
            if self.col == 7:
                self.returnList.remove([self.col+1, self.row-1])
            elif main.board[self.row-1][self.col+1] == "_":
                self.returnList.remove([self.col+1, self.row-1])
        if self.color == "Black":
            self.returnList = [                      [self.col, self.row+2],
                               [self.col-1, self.row+1], [self.col, self.row+1], [self.col+1, self.row+1]]
            if main.board[self.row+1][self.col] != "_":
                self.returnList.remove([self.col, self.row+1])
                self.returnList.remove([self.col, self.row+2])
            elif main.board[self.row+2][self.col] != "_":
                self.returnList.remove([self.col, self.row+2])
            elif self.hasMoved:
                self.returnList.remove([self.col, self.row+2])
            if self.col == 0:
                self.returnList.remove([self.col-1, self.row+1])
            elif main.board[self.row+1][self.col-1] == "_":
                self.returnList.remove([self.col-1, self.row+1])
            if self.col == 7:
                self.returnList.remove([self.col+1, self.row+1])
            elif main.board[self.row+1][self.col+1] == "_":
                self.returnList.remove([self.col+1, self.row+1])
        return self.returnList

    def Move(self, col, row):
        if inList(self.PossibleMoves(), [col, row]):
            self.col = col
            self.row = row
            if (main.board[row][col] != "_"):
                if (self.color == "White"):
                    for i in main.blackList:
                        if (i.col == self.col and i.row == self.row):
                            i.Captured()
                else:
                    for i in main.whiteList:
                        if (i.col == self.col and i.row == self.row):
                            i.Captured()
            self.hasMoved = True
            main.query()
        else:
            print("Invalid Move")


# helper function
def inList(listChecked, item):
    for i in listChecked:
        if item == i:
            return True
    return False


# move function for testing simplicity
def move(fromX, fromY, toX, toY):
    for i in main.whiteList:
        if (i.col == fromX and i.row == fromY):
            i.Move(toX, toY)
    for i in main.blackList:
        if (i.col == fromX and i.row == fromY):
            i.Move(toX, toY)


main = Board()

main.query()

print()

move(4,1,4,2)
move(3,0,6,3)
move(6,3,6,6)
move(6,6,5,7)

pygame.init()
# cool test comment 2
