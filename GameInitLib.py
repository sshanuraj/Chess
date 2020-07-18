import pygame as pg
import random
import numpy as np
import math

class Screen:
	def __init__(self, fps, frameDim):
		self.screen = pg.display.set_mode(frameDim)
		self.fps = fps
		self.clock = pg.time.Clock()
		self.con = True
		self.fontInit = pg.font.init()

	def setTextSettings(self, font, fontSize):
		return pg.font.SysFont(font, fontSize)

	def checkGameQuitState(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.endScreen()

	def putText(self, text, textObject, topLeftCoord, color, bold):
		self.screen.blit(textObject.render(text, bold, color), topLeftCoord)

	def endScreen(self):
		self.con = False

	def clockTick(self):
		self.clock.tick(self.fps)

	def keyPressedArray(self):
		return pg.key.get_pressed()

	def displayScreen(self):
		pg.display.flip()

	def screenFill(self, color):
		self.screen.fill(color)

	def getRectangle(self, dims, color, topLeftCoord): #diums =[x, y], color = (0, 0, 0), topLeftCoord = [x, y]
		pg.draw.rect(self.screen, color, (topLeftCoord[0], topLeftCoord[1], dims[0], dims[1]))

	def getCircle(self, color, center, radius):
		pg.draw.circle(self.screen, color, center, radius)

	def getRGBArray(self):
		return pg.surfarray.array3d(self.screen)

class GameEnv:
	def __init__(self, fps, frameDim):
		self.screen = Screen(fps, frameDim)
		## basic colors
		self.BLACK = (0, 0, 0)
		self.WHITE = (255, 255, 255)
		self.RED = (255, 0 , 0)
		self.GREEN = (0, 255, 0)
		self.BLUE = (0, 0, 255)
