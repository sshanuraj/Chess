import numpy as np 
import random
from ChessBoard import Board, chess
import pickle
import copy

WHITE = 1
BLACK = 0

MIN = 0
MAX = 1

INF = 100000
NINF = -100000

MAXV = 1000
MINV = -1000

"""
Piece types
chess.PAWN: chess.PieceType= 1
chess.KNIGHT: chess.PieceType= 2
chess.BISHOP: chess.PieceType= 3
chess.ROOK: chess.PieceType= 4
chess.QUEEN: chess.PieceType= 5
chess.KING: chess.PieceType= 6
"""

class Node:
    def __init__(self, parent, m, game_state):
        self.val = NINF
        self.alpha = NINF
        self.beta = INF
        self.game_state = game_state
        self.children = []
        self.agent = m
        self.moves = []
        self.parent = parent

    def resetValues(self):
    	self.val = NINF
    	self.alpha = NINF
    	self.beta = INF
    	self.children = []
    	self.agent = MAX
    	self.moves = []
    	self.parent = None

    def evaluate(self, color, colorMove):
    	w = 0
    	b = 0
    	dic = {1:1, 2:3, 3:3, 4:5, 5:9, 6:100}

    	if self.game_state.isCheckMate() and colorMove == color:
    		self.val = MAXV
    		return None
    	if self.game_state.isCheckMate() and colorMove != color:
    		self.val = MINV
    		return None

    	if self.game_state.isDraw():
    		self.val = -1
    		return None

    	for i in range(64):
    		if self.game_state.board.color_at(i) == True:
    			w = w + dic[self.game_state.board.piece_type_at(i)]
    		elif self.game_state.board.color_at(i) == False:
    			b = b + dic[self.game_state.board.piece_type_at(i)]
    	if color == WHITE:
    		self.val = w - b
    	else:
    		self.val = b - w

class GameTree:
	def __init__(self, root):
		self.root = root
	
	def getOptimumValue(self, dep, color):
		depth = 0
		k = dep
		newVal = NINF
		curr = self.root
		bestIndArr = []
		while self.root.val == NINF:
			if depth == k:
				if depth%2 == 1:
					curr.evaluate(color, color)
				else:
					curr.evaluate(color, 1 - color)
				newVal = curr.val
				
				depth -= 1
				curr = curr.parent
				continue

			if newVal > NINF:
				if curr.agent == MIN:
					if (newVal < curr.beta and len(curr.children) > 1) or len(curr.children) == 1:
						curr.beta = newVal
				else:
					if (newVal >= curr.alpha and len(curr.children) > 1) or len(curr.children) == 1:
						if curr == self.root:
							if curr.alpha < newVal:
								bestIndArr = []
								bestIndArr.append(len(curr.children) - 1)
							if curr.alpha == newVal:
								bestIndArr.append(len(curr.children) - 1)
						curr.alpha = newVal
						
				newVal = NINF

			if curr.alpha >= curr.beta:
				if curr.agent == MIN:
					curr.val = curr.beta
				else:
					curr.val = curr.alpha
				depth -= 1
				newVal = curr.val
				curr = curr.parent

			else:
				l = len(curr.children)
				cboard = copy.deepcopy(curr.game_state)
				if curr.moves == []:
					curr.moves = cboard.generateMoveStrings() 
				bf = len(curr.moves)
				if l < bf:
					cboard.makeMove(curr.moves[l])
					game_state = copy.deepcopy(cboard)
					curr.children.append(Node(curr, 1 - curr.agent, game_state))
					curr = curr.children[l]
					curr.alpha = curr.parent.alpha
					curr.beta = curr.parent.beta
					depth += 1
				else:
					if curr.agent == MIN and bf != 0:
						curr.val = curr.beta
					elif curr.agent == MIN and bf == 0:
						curr.val = MAXV
					if curr.agent == MAX and bf != 0:
						curr.val = curr.alpha
					elif curr.agent == MAX and bf == 0 :
						curr.val = MINV
					newVal = curr.val
					curr = curr.parent; depth -= 1
		print(self.root.val)
		return self.root.val, bestIndArr

	def traceRootValue(self):
		bestval = self.root.val


class ABAgent:
	def __init__(self, color):
		self.color = color
		self.gt = None

	def makeRandomMove(self, legal_moves):
		moves = []
		for move in legal_moves:
			moves.append(move)
		return moves[random.randint(0, len(moves) - 1)]

	def makeMoveUtil(self, board, depth):
		legal_moves = board.generateMoves()
		cboard = copy.deepcopy(board)
		root = Node(None, MAX, cboard)

		self.gt = GameTree(root)
		val, possibleMoves = self.gt.getOptimumValue(depth, self.color)
		moveNum = 0

		if len(possibleMoves) == 1:
			moveCnt = possibleMoves[0]
		else:
			moveCnt = possibleMoves[random.randint(0, len(possibleMoves)-1)]

		for move in legal_moves:
			if moveNum == moveCnt:
				board.makeMove(move)
				return move, val
			moveNum += 1

	def getTrace(self, maxVal):
		game_states = []
		if self.gt.root == None:
			return []

		curr = self.gt.root

		while True:
			for gs in curr.children:
				if gs.val == maxVal:
					curr = gs
					print(curr.game_state.board)
					print()
					break
			if len(curr.children) == 0:
				break

class Play:
	def __init__(self, board):
		self.board = board
		
	#desc : play both agents
	def startGame(self, W, B): #(white agent, black agent, board)
		while True:
			self.whiteMove(W)
			
			if self.board.isCheckMate():
				print("White won.")
				b.unMove()
				return 1, W, B
				
			if self.board.isDraw():
				print("Draw.")
				b.unMove()
				return 0, W, B

			print()

			self.blackMove(B)
			if self.board.isCheckMate():
				print("Black won.")
				return -1, W, B
				
			if self.board.isDraw():
				print("Draw.")
				return 0, W, B
			print()

	def whiteMove(self, W, dep):
		W.makeMoveUtil(self.board, dep)
		self.board.showBoard()
		

	def blackMove(self, B, dep):
		B.makeMoveUtil(self.board, dep)
		self.board.showBoard()

	def startGameTry(self, W, B, b):
		while True:
			W.makeMoveUtil(b, 4)
			b.showBoard()
			
			if b.isCheckMate():
				print("White won.")
				b.unMove()
				return 1, W, B
				
			if b.isDraw():
				print("Draw.")
				b.unMove()
				return 0, W, B

			print()
		
			B.makeMoveUtil(b, 2)
			b.showBoard()
			if b.isCheckMate():
				print("Black won.")
				return -1, W, B
				
			if b.isDraw():
				print("Draw.")
				return 0, W, B
			print()

	#desc: play against black		
	def play(self, B): 
		n = 1
		b = Board()

		while n:
			b.showBoard()
			moves = b.generateMoveStrings()
			print(moves)
			while True:
				move = input("Enter move:")
				#b.showBoard()
				if move in moves:
					b.makeMove(move)
					break

			if b.isCheckMate():
				b.showBoard()
				b.unMove()
				b = Board()
				n = int(input("Play again (1/0) :"))
				if n == 0:
					break
				else:
					continue
				
			if b.isDraw():
				b.showBoard()
				b.unMove()
				b = Board()
				n = int(input("Play again (1/0) :"))
				if n == 0:
					break
				
			B.makeMoveUtil(b, 1)
			#b.showBoard()
			if b.isCheckMate():
				b.showBoard()
				b = Board()
				n = int(input("Play again (1/0) :"))
				
			if b.isDraw():
				b.showBoard()
				b = Board()
				n = int(input("Play again (1/0) :"))

def evaluate(board, color, colorMove):
	w = 0
	b = 0
	dic = {1:1, 2:3, 3:3, 4:5, 5:9, 6:100}

	if board.isCheckMate() and colorMove == color:
		return MAXV
	if board.isCheckMate() and colorMove != color:
		return MINV

	if board.isDraw():
		return -1

	for i in range(64):
		if board.board.color_at(i) == True:
			w = w + dic[board.board.piece_type_at(i)]
		elif board.board.color_at(i) == False:
			b = b + dic[board.board.piece_type_at(i)]
	if color == WHITE:
		return w - b
	else:
		return b - w

# b = Board()
# B = ABAgent(BLACK)
# W = ABAgent(WHITE)
# p = Play(b)

# # p.startGame(W, B)

# b.showBoard()
# print()
# for i in range(30):
# 	print(b.generateMoveStrings())
# 	move, maxVal = W.makeMoveUtil(b, 4)
# 	print("Best move for depth 4 search for white: %s"%(move))
# 	W.getTrace(maxVal)
# 	move = input("Enter white move:")
# 	b.makeMove(move)
# 	b.showBoard()
# 	# print(evaluate(b, WHITE, BLACK)); print();
# 	print(b.generateMoveStrings())
# 	move, maxVal = B.makeMoveUtil(b, 4)
# 	print("Best move for depth 4 search for black: %s"%(move))
# 	B.getTrace(maxVal)
# 	move = input("Enter black move:")
# 	b.makeMove(move)
# 	b.showBoard()
# 	# print(evaluate(b, BLACK, WHITE)); print()
