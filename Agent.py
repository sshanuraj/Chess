import numpy as np 
import random
from ChessBoard import Board, chess

class Agent:
	def __init__(self, color, eps, alpha, df):
		self.color = color
		self.eps = eps
		self.discount_factor = df
		self.alpha = alpha
		self.state_value = {}
		self.game_states = []

	def getReward(self, reward):
		tot_reward = reward
		for i in range(len(self.game_states)-1, -1, -1):
			if self.state_value.get(self.game_states[i]) is None:
				self.state_value[self.game_states[i]] = 0.5

			if i == len(self.game_states) - 1:
				self.state_value[self.game_states[i]] = tot_reward
				continue
			
			self.state_value[self.game_states[i]] += ((self.alpha*(tot_reward - self.state_value[self.game_states[i]]))*self.discount_factor)
			tot_reward = self.state_value[self.game_states[i]]
	
	def resetState(self):
		self.game_states = []

	def decayEps(self, dec):
		self.eps = self.eps * dec

	def makeRandomMove(self, legal_moves):
		moves = []
		for move in legal_moves:
			moves.append(move)
		return moves[random.randint(0, len(moves) - 1)]

	def makeMove(self, board):
		legal_moves = board.generateMoves()
		if self.eps >= np.random.uniform(0, 1):
			move = self.makeRandomMove(legal_moves)
			board.makeMove(move)
			self.game_states.append(board.getBoardHash())
		else:
			max_val = -2
			moves = []
			print
			for move in legal_moves:
				cboard = board.board.copy()
				cboard.push(chess.Move.from_uci(str(move)))
				if cboard.is_checkmate():
					board.makeMove(move)
					self.game_states.append(board.getBoardHash())
					return
				if not self.state_value.get(cboard.fen()):
					if max_val == 0.5:
						moves.append(move)
					elif max_val < 0.5:
						moves = [] 
						moves.append(move)
						max_val = 0.5
				else:
					if max_val < self.state_value[cboard.fen()]:
						moves = []
						moves.append(move)
						max_val = self.state_value[cboard.fen()]
					elif max_val == self.state_value[cboard.fen()]:
						moves.append(move)
		
			board.makeMove(moves[random.randint(0, len(moves)-1)])
			self.game_states.append(board.board.fen())

def startGame(W, B, b):
	while True:
		W.makeMove(b)
		#b.showBoard()
		
		if b.isCheckMate():
			b.showBoard()
			b.unMove()
			W.getReward(1)
			W.resetState()
			B.getReward(0)
			B.resetState()
			return 1, W, B
			
		if b.isDraw():
			b.showBoard()
			b.unMove()
			W.getReward(0.3)
			W.resetState()
			B.getReward(0.4)
			B.resetState()
			return 0, W, B
			
		B.makeMove(b)
		#b.showBoard()
		if b.isCheckMate():
			b.showBoard()
			B.getReward(1)
			B.resetState()
			W.getReward(0)
			W.resetState()
			return -1, W, B
			
		if b.isDraw():
			b.showBoard()
			W.getReward(0.3)
			W.resetState()
			B.getReward(0.4)
			B.resetState()
			return 0, W, B
			

def train(N, W, B):
	w = 0
	bl = 0
	d = 0
	
	b = Board()
	for i in range(N):
		#print("#####Game" + str(i + 1) + "#####")
		res, W, B = startGame(W, B, b)
		#print("#####Game" + str(i + 1) + " Over#####")

		if i%10 == 0 and i != 0:
			W.decayEps(0.75)
			B.decayEps(0.75)

		if res == 1:
			print("### WHITE WON ###")
			print()
			w += 1
		elif res == -1:
			print("### BLACK WON ###")
			print()
			bl += 1
		else:
			print("### DRAW ###")
			print()
			d +=1
		b.resetBoard()
	print("White wins: " + str(w))
	print("Black wins: " + str(bl))
	print("Draws: " + str(d))
	return W, B

def play(b, B):
	n = 1
	while n:
		b.showBoard()
		print(b.generateMoveStrings())
		move = input("Enter move:")
		#b.showBoard()
		b.makeMove(move)

		if b.isCheckMate():
			b.showBoard()
			b.unMove()
			B.getReward(0)
			B.resetState()
			b.resetBoard()
			n = int(input("Play again (1/0) :"))
			if n == 0:
				break
			else:
				continue
			
		if b.isDraw():
			b.showBoard()
			b.unMove()
			W.getReward(0.3)
			W.resetState()
			B.getReward(0.4)
			B.resetState()
			b.resetBoard()
			n = int(input("Play again (1/0) :"))
			if n == 0:
				break
			
		B.makeMove(b)
		#b.showBoard()
		if b.isCheckMate():
			b.showBoard()
			B.getReward(1)
			B.resetState()
			b.resetBoard()
			n = int(input("Play again (1/0) :"))
			
		if b.isDraw():
			b.showBoard()
			B.getReward(0.4)
			B.resetState()
			b.resetBoard()
			n = int(input("Play again (1/0) :"))

W = Agent("white", 0.9, 0.9, 0.9)
B = Agent("black", 0.9, 0.9, 0.9)
W, B = train(50, W, B)
print(B.eps)
play(Board(), B)

