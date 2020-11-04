'''
Diana Ximena de León Figueroa
Carne 18607
Graficas por Computadora
Proyecto 3
'''

import pygame
from math import pi, cos, sin, atan2
import time
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LOSE = (90, 30, 5)
GRAY = (136, 136, 136)
BACKGROUND = (190, 190, 190)
INICIO = (5, 25, 40)
WIN = (60, 130, 140)

wall1 = pygame.image.load('./wall1.png')
wall2 = pygame.image.load('./wall2.png')
wall3 = pygame.image.load('./wall3.png')

enemy1 = pygame.image.load('./sprite1.png')

hand = pygame.image.load('./player.png')

flechas = pygame.image.load('./flechas.png')

textures = {
	"1": wall1,
	"2": wall2,
	"3": wall3,
}

enemies = [
	{
		"x": 100,
		"y": 150,
		"texture": enemy1
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

	def draw_rectangle(self, x, y, texture, size):
		for cx in range(x, x + size):
			for cy in range(y, y + size):
				tx = int((cx - x) * 128/size)
				ty = int((cy - y) * 128/size)
				c = texture.get_at((tx, ty))
				self.point(cx, cy, c)

	def draw_player(self, xi, yi, element, w=256, h=256):
		for x in range(xi, xi + w):
			for y in range(yi, yi + h):
				tx = int((x - xi) * 32/w)
				ty = int((y - yi) * 32/h)
				c = element.get_at((tx, ty))
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
		for i in range(0, 1000):
			try:
				a = self.player["a"] - self.player["fov"] / \
					2 + (i * self.player["fov"] / self.width)
				d, m, tx = self.cast_ray(a)
				x = i
				h = (500 / (d * cos(a - self.player["a"]))) * 50
				self.draw_stake(x, h, tx, textures[m])
			except:
				self.player["x"] = self.blocksize + 20
				self.player["y"] = self.blocksize + 20
				self.game_over()

		for enemy in enemies:
			self.point(enemy["x"], enemy["y"], BLACK)
			self.draw_sprite(enemy)
		
		for x in range(0, 100, 10):
			for y in range(0, 100, 10):
				i = int(x/10)
				j = int(y/10)
				if self.map[j][i] != ' ':
					y = 500 + y
					x1 = 900 + x
					self.draw_rectangle(x1, y, textures[self.map[j][i]], 10)

		self.point(int(self.player["x"] * 0.2) + 900, int(self.player["y"] * 0.2) + 500, LOSE)
		
		self.draw_player(1000 - 256 - 128 - 150, 500 - 256, hand)

	def text_objects(self, text, font):
		textSurface = font.render(text, True, WHITE)
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

			gameDisplay.fill(INICIO)
			largeText = pygame.font.Font('freesansbold.ttf', 75)
			mediumText = pygame.font.Font('freesansbold.ttf', 35)
			smallText = pygame.font.Font('freesansbold.ttf', 15)
			TextSurf, TextRect = self.text_objects(
				"PROYECTO RAYCASTER", largeText)
			TextRect.center = (int(1000/2), int(500/2))
			gameDisplay.blit(TextSurf, TextRect)
			TextSurf, TextRect = self.text_objects(
				"PRESIONE Q PARA EMPEZAR", mediumText)
			TextRect.center = (int(1000/2), int(700/2))
			gameDisplay.blit(TextSurf, TextRect)
			TextSurf, TextRect = self.text_objects(
				"ESC PARA SALIR", smallText)
			TextRect.center = (int(1000/2), int(900/2))
			gameDisplay.blit(TextSurf, TextRect)
			pygame.display.update()
			clock.tick(15)

	def game_over(self):
		lose_sound = pygame.mixer.Sound('./perder.wav')
		pygame.mixer.Sound.play(lose_sound)
		pygame.mixer.music.stop()
		
		intro = True
		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					exit(0)
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						intro = False
						self.game_intro()

			gameDisplay.fill(LOSE)
			largeText = pygame.font.Font('freesansbold.ttf', 75)
			mediumText = pygame.font.Font('freesansbold.ttf', 35)
			smallText = pygame.font.Font('freesansbold.ttf', 15)
			TextSurf, TextRect = self.text_objects("GAME OVER", largeText)
			TextRect.center = (int(1000/2), int(500/2))
			gameDisplay.blit(TextSurf, TextRect)
			TextSurf, TextRect = self.text_objects(
				"PRESIONE R PARA REINICIAR", mediumText)
			TextRect.center = (int(1000/2), int(700/2))
			gameDisplay.blit(TextSurf, TextRect)
			TextSurf, TextRect = self.text_objects(
				"ESC PARA SALIR", smallText)
			TextRect.center = (int(1000/2), int(900/2))
			gameDisplay.blit(TextSurf, TextRect)
			pygame.display.update()
			clock.tick(15)

	def game_win(self):
		win_sound = pygame.mixer.Sound('./ganar.wav')
		pygame.mixer.Sound.play(win_sound)
		pygame.mixer.music.stop()
		
		intro = True
		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					exit(0)
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						intro = False
						self.game_intro()

			gameDisplay.fill(WIN)
			largeText = pygame.font.Font('freesansbold.ttf', 60)
			mediumText = pygame.font.Font('freesansbold.ttf', 35)
			smallText = pygame.font.Font('freesansbold.ttf', 15)
			TextSurf, TextRect = self.text_objects(
				"NICE JOB, YOU WON", largeText)
			TextRect.center = (int(1000/2), int(500/2))
			gameDisplay.blit(TextSurf, TextRect)
			TextSurf, TextRect = self.text_objects(
				"PRESIONE R PARA REINICIAR", mediumText)
			TextRect.center = (int(1000/2), int(700/2))
			gameDisplay.blit(TextSurf, TextRect)
			TextSurf, TextRect = self.text_objects(
				"ESC PARA SALIR", smallText)
			TextRect.center = (int(1000/2), int(900/2))
			gameDisplay.blit(TextSurf, TextRect)
			pygame.display.update()
			clock.tick(15)

	def sound(self):
		pygame.mixer.music.load('./fondo.wav')
		pygame.mixer.music.set_volume(0.8)
		pygame.mixer.music.play(-1)

	def game_start(self):
		fuente = pygame.font.Font(None, 25)
		clock = pygame.time.Clock()
		paused = False
		running = True
		while running:
			screen.fill(BACKGROUND)
			d = 10
			clock.tick(10)
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
						elif e.key == pygame.K_s: 
							r.sound()
					if e.key == pygame.K_SPACE:
						paused = not paused
				if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
					if not paused:
						if e.button == 4:
							r.player['a'] -= pi/20
						if e.button == 5:
							r.player['a'] += pi/20
			if not paused:
				texto_de_salida = "FPS: " + str(round(clock.get_fps(), 2))
				texto = fuente.render(texto_de_salida, True, WHITE)
				screen.blit(texto, [600, 550])
				if (r.player["x"] >= 400 and r.player["x"] <= 420) and (r.player["y"] >= 250 and r.player["y"] <= 265):
					self.game_win() 
				r.render()
				pygame.display.flip()

			
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((1000, 600))
screen.set_alpha(None)
r = Raycaster(screen)
r.load_map('./map.txt')
gameDisplay = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('Raycaster - Proyecto 3')
clock = pygame.time.Clock()
r.game_intro()
