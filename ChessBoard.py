import chess

class Board:
	def __init__(self):
		self.board = chess.Board()

	def makeMove(self, move):
		self.board.push(chess.Move.from_uci(str(move)))

	def generateMoves(self):
		return self.board.legal_moves

	def generateMoveStrings(self):
		moves= [] 
		for move in self.board.legal_moves:
			moves.append(move)
		print(moves)

	def showBoard(self):
		print(self.board)

	def unMove(self):
		self.board.pop()

	def isCheckMate(self):
		return self.board.is_checkmate()

	def isDraw(self):
		if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_fivefold_repetition() or self.board.is_seventyfive_moves():
			return True
		return False

	def resetBoard(self):
		self.board.reset_board()

	def getBoardHash(self):
		return self.board.fen()

# b = Board()
# b.resetBoard()
# print(b.generateMoves())
# b.makeMove("e2e4")
# b.showBoard()
# b.unMove()
# b.resetBoard()
# print(b.generateMoves())
# b.makeMove("e2e4")
# b.showBoard()
# b.makeMove("e7e5")
# b.showBoard()


