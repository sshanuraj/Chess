from ChessBoard import Board 
import GameInitLib as gil 
import ABAgent as agent
import time

class Chess:
	def __init__(self, w_agent, b_agent, board, gameEnv):
		self.w_agent = w_agent
		self.b_agent = b_agent
		self.board = board
		self.gameEnv = gameEnv
		self.start = agent.Play(self.board)

	def setBoard(self):
		x = 0
		y = 0
		piecesW = ["", "P", "N", "B", "R", "Q", "K"]
		piecesB = ["", "p", "n", "b", "r", "q", "k"]
		textObject = self.gameEnv.screen.setTextSettings("Tahoma", 20)
		self.gameEnv.screen.screenFill(self.gameEnv.BLACK)

		for i in range(8):
			if i%2 == 0:
				x = 0
				y = 50*i
			else:
				x = 50
				y = 50*i
			for j in range(4):
				dims = [50, 50]
				color = self.gameEnv.WHITE
				topLeftCoord = [x, y]
				self.gameEnv.screen.getRectangle(dims, color, topLeftCoord)
				x += 100

		y = 412
		for i in range(64):
			if i%8 == 0:
				x = 15
				y = y - 50
			if self.board.board.color_at(i) == True:
				self.gameEnv.screen.putText(piecesW[self.board.board.piece_type_at(i)], textObject, (x, y), self.gameEnv.RED, True)
			elif self.board.board.color_at(i) == False:
				self.gameEnv.screen.putText(piecesB[self.board.board.piece_type_at(i)], textObject, (x, y), self.gameEnv.RED, True)
			x = x + 50

	def initBoard(self):
		self.setBoard()
		self.gameEnv.screen.displayScreen()
		move = 0
		while self.gameEnv.screen.con:
			self.gameEnv.screen.checkGameQuitState()
			if move%2 == 0:
				self.start.whiteMove(self.w_agent, 3)

				if self.board.isCheckMate():
					print("White won.")
					b.unMove()
					self.gameEnv.screen.endScreen()
					
				if self.board.isDraw():
					print("Draw.")
					b.unMove()
					self.gameEnv.screen.endScreen()
				self.setBoard()
			else:
				self.start.blackMove(self.b_agent, 3)
				if self.board.isCheckMate():
					print("Black won.")
					b.unMove()
					self.gameEnv.screen.endScreen()
					
				if self.board.isDraw():
					print("Draw.")
					b.unMove()
					self.gameEnv.screen.endScreen()
				self.setBoard()
			move += 1
			self.gameEnv.screen.displayScreen()
			self.gameEnv.screen.clockTick()


gameEnv = gil.GameEnv(30, (400, 400))
W = agent.ABAgent(agent.WHITE)
B = agent.ABAgent(agent.BLACK)
b = Board()
chess = Chess(W, B, b, gameEnv)
chess.initBoard()

