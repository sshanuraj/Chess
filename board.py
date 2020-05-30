import numpy as np 
from piece import *

class Board:
	def __init__(self):
		self.board = []
		self.pieceToPosition = {}
		self.pieceToPieceObj = {}
		self.resetBoard()

	def resetBoard(self):
		self.board = []
		
		self.board.append(["br1", "bn1", "bb1", "bq", "bk", "bb2", "bn2", "br2"])
		self.board.append(["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8"])
		
		empty_array = ["--", "--", "--", "--", "--", "--", "--", "--"]
		for i in range(4):
			self.board.append(empty_array.copy())

		self.board.append(["w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8"])
		self.board.append(["wr1", "wn1", "wb1", "wq", "wk", "wb2", "wn2", "wr2"])

		for i in range(8):
			for j in range(8):
				self.pieceToPosition[self.board[i][j]] = [i, j]
				if self.board[i][j][0] == 'w':
					if len(self.board[i][j]) == 2:
						if self.board[i][j][1] == 'k':
							self.pieceToPieceObj[self.board[i][j]] = King("king", [i, j], "white")
						elif self.board[i][j][1] == 'q':
							self.pieceToPieceObj[self.board[i][j]] = Piece("queen", [i, j], "white")
						else:
							self.pieceToPieceObj[self.board[i][j]] = Pawn("pawn", [i, j], "white")
					else:
						if self.board[i][j][1] == 'r':
							self.pieceToPieceObj[self.board[i][j]] = Piece("rook", [i, j], "white")
						elif self.board[i][j][1] == 'b':
							self.pieceToPieceObj[self.board[i][j]] = Piece("bishop", [i, j], "white")
						elif self.board[i][j][1] == 'n':
							self.pieceToPieceObj[self.board[i][j]] = Piece("knight", [i, j], "white")
				elif self.board[i][j][0] == 'b':
					if len(self.board[i][j]) == 2:
						if self.board[i][j][1] == 'k':
							self.pieceToPieceObj[self.board[i][j]] = King("king", [i, j], "black")
						elif self.board[i][j][1] == 'q':
							self.pieceToPieceObj[self.board[i][j]] = Piece("queen", [i, j], "black")
						else:
							self.pieceToPieceObj[self.board[i][j]] = Pawn("pawn", [i, j], "black")
					else:
						if self.board[i][j][1] == 'r':
							self.pieceToPieceObj[self.board[i][j]] = Piece("rook", [i, j], "black")
						elif self.board[i][j][1] == 'b':
							self.pieceToPieceObj[self.board[i][j]] = Piece("bishop", [i, j], "black")
						elif self.board[i][j][1] == 'n':
							self.pieceToPieceObj[self.board[i][j]] = Piece("knight", [i, j], "black")
				else:
					self.pieceToPieceObj[self.board[i][j]] = None

	def printBoard(self):
		dic = {"wr1" : "WR", "wr2" : "WR", "wn1" : "WN", "wn2" : "WN", "wb1" : "WB" , "wb2" : "WB", "wk" : "WK", "wq" : "WQ", "br1" : "BR", "br2" : "BR", "bn1" : "BN", "bn2" : "BN", "bb1" : "BB", "bb2" : "BB", "bk" : "BK", "bq" : "BQ"}

		for i in range(8):
			for j in range(8):
				if dic.get(self.board[i][j]):
					print(dic[self.board[i][j]] + " ", end = " ")
				else:
					print(self.board[i][j] + " ", end = " ")
			print()

	def getPiecePosition(self, piece):
		pos = self.pieceToPosition[piece]
		return chr(97 + pos[1]) + str(8 - pos[0])

	def isCheck(self, color):
		if color == "white":
			bkpos = self.pieceToPieceObj["bk"].position
			for keys in self.pieceToPieceObj.keys():
				piece = self.pieceToPieceObj[keys]
				if keys[0] == 'w':
					if keys[1] == 'r':
						if bkpos in piece.generateRookScope(self.board):
							return True
					elif keys[1] == 'q':
						if bkpos in piece.generateQueenScope(self.board):
							return True
					elif keys[1] == 'b':
						if bkpos in piece.generateBishopScope(self.board):
							return True
					elif keys[1] == 'n':
						if bkpos in piece.generateKnightScope(self.board):
							return True
					else:
						if bkpos in piece.generatePawnCaptureScope(self.board):
							return True
		else:
			bkpos = self.pieceToPieceObj["wk"].position
			for keys in piecetoPieceObj.keys():
				piece = self.pieceToPieceObj[keys]
				if keys[0] == 'b':
					if keys[1] == 'r':
						if bkpos in piece.generateRookScope(self.board):
							return True
					elif keys[1] == 'q':
						if bkpos in piece.generateQueenScope(self.board):
							return True
					elif keys[1] == 'b':
						if bkpos in piece.generateBishopScope(self.board):
							return True
					elif keys[1] == 'n':
						if bkpos in piece.generateKnightScope(self.board):
							return True
					else:
						if bkpos in piece.generatePawnCaptureScope(self.board):
							return True
		return False

	def isCheckMate(self, board):
		return True

	def makeMove(self, init_pos, final_pos, color):
		pieceInitial = self.board[init_pos[0]][init_pos[1]]
		pieceFinal = self.board[final_pos[0]][final_pos[1]]

		pObjInit = self.pieceToPieceObj[pieceInitial]
		pObjFinal = self.pieceToPieceObj[pieceFinal]

		if pObjFinal == None:
			self.pieceToPieceObj[pieceInitial].position = final_pos

		
b = Board()
b.printBoard()

print(b.isCheck("white"))

