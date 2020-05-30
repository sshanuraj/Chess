import numpy as np

class Piece:
	def __init__(self, name, position, color):
		self.name = name
		self.color = color
		self.position = position
		self.canCastle = False
		self.canMove2 = False
		self.canEnPassant = False

	def oppositeColor(self):
		if self.color[0] == 'w':
			return 'b'
		return 'w'

	def checkPosition(self, x, y):
		if (x <= -1 or x >= 8) or (y >= 8 or y <= -1):
			return False
		return True

	def generatePawnCaptureScope(self, board):
		move_scope = []
		pos = self.position

		if self.color == "white":
			#left capture
			if self.checkPosition(pos[0] - 1, pos[1] - 1):
				move_scope.append([pos[0] - 1, pos[1] - 1])
			#right capture
			if self.checkPosition(pos[0] - 1, pos[1] + 1):
				move_scope.append([pos[0] - 1, pos[1] + 1])
		else:
			#left captue
			if self.checkPosition(pos[0] + 1, pos[1] - 1):
				move_scope.append(pos[0] + 1, pos[1] - 1)
			if self.checkPosition(pos[0] + 1, pos[1] + 1):
				move_scope.append(pos[0] + 1, pos[1] + 1)
		return move_scope

	def generatePawnScope(self, board):
		move_scope = []
		pos = self.position

		if self.color == "white":
			#one move forward check
			if pos[0] + 1 <= 7 and board[pos[0] - 1][pos[1]] == "--":
				move_scope.append([pos[0] - 1, pos[1]])
			#two move forward check
			if self.canMove2 and board[pos[0] - 2][pos[1]] == "--":
				move_scope.append([pos[0] - 2, pos[1]])
			#check for captures on left
			if self.checkPosition(pos[0] - 1, pos[1] - 1) and board[pos[0] - 1][pos[1] - 1][0] == "b":
				move_scope.append([pos[0] - 1, pos[0] - 1])
			#check for captures on right
			if self.checkPosition(pos[0]-1, pos[1]+1) and board[pos[0]-1][pos[1]+1][0] == "b":
				move_scope.append([pos[0]-1, pos[1]+1])

		else:
			#one move forward check
			if self.checkPosition(pos[0] + 1, pos[1]) and board[pos[0] + 1][pos[1]] == "--":
				move_scope.append([pos[0] + 1, pos[1]])
			#two move forward check
			if self.canMove2 and board[pos[0] + 2][pos[1]] == "--":
				move_scope.append([pos[0] + 2, pos[1]])
			#check for captures on left
			if self.checkPosition(pos[0] + 1, pos[1] - 1) and board[pos[0] + 1][pos[1] - 1][0] == "w":
				move_scope.append([pos[0] + 1, pos[0] - 1])
			#check for captures on right
			if self.checkPosition(pos[0] + 1, pos[1] + 1) and board[pos[0] + 1][pos[1] + 1][0] == "w":
				move_scope.append([pos[0] + 1, pos[1] + 1])
		return move_scope

	def generateRookScope(self, board):
		move_scope = []
		pos = self.position
		x = pos[0]; y = pos[1];

		while True:  #going down
			x = x + 1
			if not self.checkPosition(x, y):
				break
			if board[x][y] == "--":
				move_scope.append([x, y])
			else:
				if board[x][y][0] == self.oppositeColor():
					move_scope.append([x, y])
				break;

		x = pos[0]; y = pos[1];
		while True:  #going up
			x = x-1
			if not self.checkPosition(x, y):
				break
			if board[x][y] == "--":
				move_scope.append([x, y])
			else:
				if board[x][y][0] == self.oppositeColor():
					move_scope.append([x, y])
				break

		x = pos[0]; y = pos[1];
		while True: # going right
			y=y+1
			if not self.checkPosition(x,y):
				break
			if board[x][y] == "--":
				move_scope.append([x, y])
			else:
				if board[x][y][0] == self.oppositeColor():
					move_scope.append([x, y])
				break

		x = pos[0]; y = pos[1];
		while True: # going right
			y=y-1
			if not self.checkPosition(x,y):
				break
			if board[x][y] == "--":
				move_scope.append([x, y])
			else:
				if board[x][y][0] == self.oppositeColor():
					move_scope.append([x, y])
				break

		return move_scope

	def generateKingScope(self, board):
		move_scope = []
		pos = self.position
		x = pos[0]; y = pos[1];

		if self.checkPosition(x+1, y+1) and (board[x+1][y+1] == "--" or board[x+1][y+1][0] == self.oppositeColor()):
			move_scope.append([x+1, y+1])
		if self.checkPosition(x+1, y) and (board[x+1][y] == "--" or board[x+1][y][0] == self.oppositeColor()):
			move_scope.append([x+1, y])
		if self.checkPosition(x+1, y-1) and (board[x+1][y-1] == "--" or board[x+1][y-1][0] == self.oppositeColor()):
			move_scope.append([x+1, y-1])
		if self.checkPosition(x, y+1) and (board[x][y+1] == "--" or board[x][y+1][0] == self.oppositeColor()):
			move_scope.append([x, y+1])
		if self.checkPosition(x, y-1) and (board[x][y-1] == "--" or board[x][y-1][0] == self.oppositeColor()):
			move_scope.append([x, y-1])
		if self.checkPosition(x-1, y) and (board[x-1][y] == "--" or board[x-1][y][0] == self.oppositeColor()):
			move_scope.append([x-1, y])
		if self.checkPosition(x-1, y-1) and (board[x-1][y-1] == "--" or board[x-1][y-1][0] == self.oppositeColor()):
			move_scope.append([x-1, y-1])
		if self.checkPosition(x-1, y+1) and (board[x-1][y+1] == "--" or board[x-1][y+1][0] == self.oppositeColor()):
			move_scope.append([x-1, y+1])

		return move_scope

	def generateBishopScope(self, board):
		move_scope = []
		pos = self.position

		x = pos[0]; y = pos[1];
		while True:
			x = x + 1
			y = y + 1
			if not self.checkPosition(x, y):
				break
			if board[x][y] == "--":
				move_scope.append([x, y])
			else:
				if board[x][y][0] == self.oppositeColor():
					move_scope.append([x, y])
				break

		x = pos[0]; y = pos[1]
		while True:
			x = x + 1
			y = y - 1
			if not self.checkPosition(x, y):
				break;
			if board[x][y] == "--":
				move_scope.append([x, y])
			else:
				if board[x][y][0] == self.oppositeColor():
					move_scope.append([x, y])
				break

		x = pos[0]; y = pos[1];
		while True:
			x = x - 1
			y = y - 1
			if not self.checkPosition(x, y):
				break;
			if board[x][y] == "--":
				move_scope.append([x, y])
			else:
				if board[x][y][0] == self.oppositeColor():
					move_scope.append([x, y])
				break
		x = pos[0]; y = pos[1];
		while True:
			x = x - 1
			y = y + 1
			if not self.checkPosition(x, y):
				break;
			if board[x][y] == "--":
				move_scope.append([x, y])
			else:
				if board[x][y][0] == self.oppositeColor():
					move_scope.append([x, y])
				break
		return move_scope

	def generateKnightScope(self, board):
		move_scope = []
		pos = self.position
		x = pos[0]; y = pos[1];
		if self.checkPosition(x+2, y+1) and (board[x+2][y+1] == "--" or board[x+2][y+1][0] == self.oppositeColor()):
			move_scope.append([x+2, y+1])

		if self.checkPosition(x+2, y-1) and (board[x+2][y-1] == "--" or board[x+2][y-1][0] == self.oppositeColor()):
			move_scope.append([x+2, y-1])

		if self.checkPosition(x-2, y+1) and (board[x-2][y+1] == "--" or board[x-2][y+1][0] == self.oppositeColor()):
			move_scope.append([x-2, y+1])

		if self.checkPosition(x-2, y-1) and (board[x-2][y-1] == "--" or board[x-2][y-1][0] == self.oppositeColor()):
			move_scope.append([x-2, y-1])

		if self.checkPosition(x+1, y+2) and (board[x+1][y+2] == "--" or board[x+1][y+2][0] == self.oppositeColor()):
			move_scope.append([x+1, y+2])

		if self.checkPosition(x+1, y-2) and (board[x+1][y-2] == "--" or board[x+1][y-2][0] == self.oppositeColor()):
			move_scope.append([x+1, y-2])

		if self.checkPosition(x-1, y+2) and (board[x-1][y+2] == "--" or board[x-1][y+2][0] == self.oppositeColor()):
			move_scope.append([x-1, y+2])

		if self.checkPosition(x-1, y-2) and (board[x-1][y-2] == "--" or board[x-1][y-2][0] == self.oppositeColor()):
			move_scope.append([x-1, y-2])

		return move_scope

	def generateQueenScope(self, board):
		move_scope = self.generateRookScope(board) + self.generateBishopScope(board)
		return move_scope

class King(Piece):
	def __init__(self, name, position, color):
		super().__init__(name, position, color)
		self.canCastle = True


class Pawn(Piece):
	def __init__(self, name, position, color):
		super().__init__(name, position, color)
		self.canMove2 = True