'''
Diana Ximena de León Figueroa
Carne 18607
Graficas por Computadora
Laboratorio #4 UI
'''

import pygame
from math import pi, cos, sin, atan2
import time
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 30, 15)
GRAY = (136, 136, 136)
BACKGROUND = (0, 255, 255)
YELLOW = (255, 165, 15)
GREEN = (5, 220, 20)

colors = {
	"1": (255, 0, 0),
	"2": (0, 255, 0),
	"3": (0, 0, 255)
}

wall1 = pygame.image.load('./wall1.png')
wall2 = pygame.image.load('./wall2.png')
wall3 = pygame.image.load('./wall3.png')
wall4 = pygame.image.load('./wall4.png')
wall5 = pygame.image.load('./wall5.png')

enemy1 = pygame.image.load('./sprite1.png')
enemy2 = pygame.image.load('./sprite2.png')
enemy3 = pygame.image.load('./sprite3.png')
enemy4 = pygame.image.load('./sprite4.png')

hand = pygame.image.load('./player.png')

sword1 = pygame.image.load('./sword.png')

textures = {
	"1": wall1,
	"2": wall2,
	"3": wall3,
	"4": wall4,
	"5": wall5,
}

enemies = [
	{
		"x": 100,
		"y": 150,
		"texture": enemy1
	}
]

swords = [
	{
		"x": 200,
		"y": 70,
		"texture": sword1,
		'touch': False
	},
	{
		"x": 300,
		"y": 70,
		"texture": sword1,
		'touch': False
	},
	{
		"x": 400,
		"y": 70,
		"texture": sword1,
		'touch': False
	}
]


class Raycaster:
	def __init__(self, screen):
		_, _, self.width, self.height = screen.get_rect()
		self.screen = screen
		self.blocksize = 50
		self.map = []
		self.zbuffer = [-float('inf') for z in range(0, 500)]
		self.player = {
			"x": self.blocksize + 20,
			"y": self.blocksize + 20,
			"a": 0,
			"fov": pi/3
		}

	def point(self, x, y, c=None):
		screen.set_at((x, y), c)

	def draw_rectangle(self, x, y, texture):
		for cx in range(x, x + 50):
			for cy in range(y, y + 50):
				tx = int((cx - x) * 128/50)
				ty = int((cy - y) * 128/50)
				c = texture.get_at((tx, ty))
				self.point(cx, cy, c)

	def draw_player(self, xi, yi, w=256, h=256):
		for x in range(xi, xi + w):
			for y in range(yi, yi + h):
				tx = int((x - xi) * 32/w)
				ty = int((y - yi) * 32/h)
				c = hand.get_at((tx, ty))
				if c != (152, 0, 136, 255):
					self.point(x, y, c)

	def load_map(self, filename):
		with open(filename) as f:
			for line in f.readlines():
				self.map.append(list(line))

	def cast_ray(self, a):
		d = 0
		while True:
			x = int(self.player["x"] + d * cos(a))
			y = int(self.player["y"] + d * sin(a))

			i = int(x / self.blocksize)
			j = int(y / self.blocksize)

			if self.map[j][i] != ' ':
				hitx = x - i * 50
				hity = y - j * 50
				if 1 < hitx < 49:
					maxhit = hitx
				else:
					maxhit = hity
				tx = int(maxhit * 128 / 50)
				return d, self.map[j][i], tx
			self.point(x, y, WHITE)
			d += 1

	def draw_stake(self, x, h, tx, texture):
		start = int(250 - h/2)
		end = int(250 + h/2)
		for y in range(start, end):
			ty = int((y - start) * (128 / (end - start)))
			c = texture.get_at((tx, ty))
			self.point(x, y, c)

	def draw_sprite(self, sprite):
		sprite_a = atan2((sprite["y"] - self.player["y"]),
						 (sprite["x"] - self.player["x"]))
		sprite_d = ((self.player["x"] - sprite["x"]) ** 2 +
					(self.player["y"] - sprite["y"]) ** 2) ** 0.5
		sprite_size = int(500/sprite_d * 70)
		sprite_x = int(500 + (sprite_a - self.player["a"]) * 500/self.player["fov"] +
					   250 - sprite_size/2)
		sprite_y = int(250 - sprite_size/2)

		for x in range(sprite_x, sprite_x + sprite_size):
			for y in range(sprite_y, sprite_y + sprite_size):
				if 500 < x < 1000 and self.zbuffer[x - 500] <= sprite_d:
					tx = int((x - sprite_x) * 128/sprite_size)
					ty = int((y - sprite_y) * 128/sprite_size)
					c = sprite["texture"].get_at((tx, ty))
					if c != (152, 0, 136, 255):
						self.point(x, y, c)
						self.zbuffer[x - 500] = sprite_d

	def render(self):
		for x in range(0, int(self.width / 2), self.blocksize):
			for y in range(0, self.height, self.blocksize):
				i = int(x/self.blocksize)
				j = int(y/self.blocksize)
				if self.map[j][i] != ' ':
					self.draw_rectangle(x, y, textures[self.map[j][i]])

		self.point(self.player["x"], self.player["y"], WHITE)

		for i in range(0, 500):
			try:
				a = self.player["a"] - self.player["fov"] / \
					2 + (i * self.player["fov"] / 500)
				d, m, tx = self.cast_ray(a)
				x = 500 + i
				h = (500 / (d * cos(a - self.player["a"]))) * 50
				self.draw_stake(x, h, tx, textures[m])
			except:
				pass

		for i in range(0, 500):
			self.point(499, i, (0, 0, 0))
			self.point(500, i, (0, 0, 0))
			self.point(501, i, (0, 0, 0))

		for enemy in enemies:
			self.point(enemy["x"], enemy["y"], BLACK)
			self.draw_sprite(enemy)

		for sword in swords:
			if sword["touch"] == False:
				self.point(sword["x"], sword["y"], BLACK)
				self.draw_sprite(sword)

		self.draw_player(1000 - 256 - 128, 500 - 256)

	def text_objects(self, text, font):
		textSurface = font.render(text, True, BLACK)
		return textSurface, textSurface.get_rect()

	def game_intro(self):
		intro = True

		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					exit(0)
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						intro = False
						self.game_start()

			gameDisplay.fill(YELLOW)
			largeText = pygame.font.Font('freesansbold.ttf', 75)
			mediumText = pygame.font.Font('freesansbold.ttf', 35)
			smallText = pygame.font.Font('freesansbold.ttf', 15)
			TextSurf, TextRect = self.text_objects(
				"Laboratorio #4 - UI", largeText)
			TextRect.center = (int(1000/2), int(400/2))
			gameDisplay.blit(TextSurf, TextRect)
			TextSurf, TextRect = self.text_objects(
				"Q para empezar el juego", mediumText)
			TextRect.center = (int(1000/2), int(600/2))
			gameDisplay.blit(TextSurf, TextRect)
			TextSurf, TextRect = self.text_objects(
				"ESC para salir", smallText)
			TextRect.center = (int(1000/2), int(800/2))
			gameDisplay.blit(TextSurf, TextRect)
			pygame.display.update()
			clock.tick(15)

	def game_over(self):
		intro = True

		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					exit(0)
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						intro = False
						self.game_intro()

			gameDisplay.fill(RED)
			largeText = pygame.font.Font('freesansbold.ttf', 75)
			mediumText = pygame.font.Font('freesansbold.ttf', 35)
			smallText = pygame.font.Font('freesansbold.ttf', 15)
			TextSurf, TextRect = self.text_objects("GAME OVER", largeText)
			TextRect.center = (int(1000/2), int(400/2))
			gameDisplay.blit(TextSurf, TextRect)
			TextSurf, TextRect = self.text_objects(
				"R para reiniciar", mediumText)
			TextRect.center = (int(1000/2), int(600/2))
			gameDisplay.blit(TextSurf, TextRect)
			TextSurf, TextRect = self.text_objects(
				"ESC para salir", smallText)
			TextRect.center = (int(1000/2), int(800/2))
			gameDisplay.blit(TextSurf, TextRect)
			pygame.display.update()
			clock.tick(15)

	def game_win(self):
		intro = True
		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					exit(0)
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						intro = False
						self.game_intro()

			gameDisplay.fill(GREEN)
			largeText = pygame.font.Font('freesansbold.ttf', 60)
			mediumText = pygame.font.Font('freesansbold.ttf', 35)
			smallText = pygame.font.Font('freesansbold.ttf', 15)
			TextSurf, TextRect = self.text_objects(
				"Congratulations, YOU WON", largeText)
			TextRect.center = (int(1000/2), int(400/2))
			gameDisplay.blit(TextSurf, TextRect)
			TextSurf, TextRect = self.text_objects(
				"R para reiniciar", mediumText)
			TextRect.center = (int(1000/2), int(600/2))
			gameDisplay.blit(TextSurf, TextRect)
			TextSurf, TextRect = self.text_objects(
				"ESC para salir", smallText)
			TextRect.center = (int(1000/2), int(800/2))
			gameDisplay.blit(TextSurf, TextRect)
			pygame.display.update()
			clock.tick(15)

	def game_start(self):

		fuente = pygame.font.Font(None, 25)
		swords_count = 0

		paused = False
		running = True
		while running:
			screen.fill((0, 0, 0))
			d = 10
			for e in pygame.event.get():
				if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
					running = False
					exit(0)
				if e.type == pygame.KEYDOWN:
					if not paused:
						if e.key == pygame.K_LEFT:
							r.player["a"] -= pi/20
						if e.key == pygame.K_RIGHT:
							r.player["a"] += pi/20
						if e.key == pygame.K_UP:
							r.player["x"] += int(d * cos(r.player["a"]))
							r.player["y"] += int(d * sin(r.player["a"]))
						if e.key == pygame.K_DOWN:
							r.player["x"] -= int(d * cos(r.player["a"]))
							r.player["y"] -= int(d * sin(r.player["a"]))
						if (r.player["x"] > 75 and r.player["x"] < 125) and (r.player["y"] > 125 and r.player["y"] < 175):
							self.game_over()
						if (r.player["x"] > 190 and r.player["x"] < 210) and (r.player["y"] == 70):
							swords[0]["touch"] = True
							swords_count += 1
						if (r.player["x"] > 290 and r.player["x"] < 310) and (r.player["y"] == 70):
							swords[1]["touch"] = True
							swords_count += 1
						if (r.player["x"] > 390 and r.player["x"] < 410) and (r.player["y"] == 70):
							swords[2]["touch"] = True
							swords_count += 1
					if e.key == pygame.K_SPACE:
						paused = not paused
			if not paused:
				texto_de_salida = "Swords count:" + str(swords_count)
				texto = fuente.render(texto_de_salida, True, WHITE)
				screen.blit(texto, [600, 20])
				if swords_count == 3:
					self.game_win()
				r.render()
				pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((1000, 500))
screen.set_alpha(None)
r = Raycaster(screen)
r.load_map('./map.txt')
gameDisplay = pygame.display.set_mode((1000, 500))
pygame.display.set_caption('Laboratorio 4 - UI')
clock = pygame.time.Clock()
r.game_intro()
