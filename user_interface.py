#10525263 Ethan Wong
#project5.py

'''
This script implements the "view" for the
Columns Game.
'''

import pygame
import columns
import random

_INITIAL_WIDTH = 700
_INITIAL_HEIGHT = 700
_FRAME_RATE = 30

_BOARD_ROWS = 13
_BOARD_COLUMNS = 6

_WHITE = pygame.Color(255, 255, 255)
_BACKGROUND_COLOR = pygame.Color(210, 249, 249)
_COLORS = {
'S': pygame.Color(255, 0 , 0),
'T': pygame.Color(255, 0 , 223),
'V': pygame.Color(113, 0 , 255),
'W': pygame.Color(0, 73 , 255),
'X': pygame.Color(0, 251 , 255),
'Y': pygame.Color(0, 255 , 0),
'Z': pygame.Color(243, 255 , 0),
}

_HORIZONTAL_GRID_FRAC_POINTS = [(0.4, 0.175), (0.7, 0.175)]
_VERTICAL_GRID_FRAC_POINTS = [(0.4, 0.175), (0.4, 0.825)]


class ColumnsGame:
	'''
	This class manages the overall running and related methods needed
	to smoothly implement the view of the Columns game.
	'''
	def __init__(self):
		self._colors = [234, 150, 150, 1, 2]
			#first three values represent color values
			#last two represent position and direction to increment
		self._running = True
		self._counter = 0 #used keep falling at one second


	def run(self):
		pygame.init()
		try:
			self._clock = pygame.time.Clock()
			self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))
			self._initialize_game()
			while self._running:
				self._clock.tick(_FRAME_RATE)
				self._handle_events() #handles events from the window / user input

				if self._counter == _FRAME_RATE-10:
					#ensures falling and matching occur at a rate visible to the eye
					#	of once per second
					if self._game_state.check_matches():
						self._game_state.remove_matches()
					else:
						self._game_state.tick_time()
					self._counter = 0
				elif self._game_state.check_matches():
					pass
				elif (self._game_state.get_faller() == None) or (self._game_state.get_faller().get_state() == columns.EMPTY):
					self._make_random_faller()

				#self._print_board()
				self._draw_board()
				self._check_game_over()
				self._counter += 1
		finally:
			pygame.quit()

	def _check_game_over(self) -> None:
		'''
		This method checks if the game is over
		and ends the game when it is by closing
		the pygame window and printing a message to the console.
		'''
		if self._game_state.is_game_over():
			print('GAME OVER')
			quit()

	def _create_surface(self, size:(int, int)):
		'''
		This method creates a resizable surface
		for drawing on throughout the animation 
		of the Columns game.
		'''
		self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)

	def _handle_events(self):
		'''
		This handles all the events that have happened
		within the last tick of the pygame Clock.
		'''
		for event in pygame.event.get():
			self._handle_event(event)

	def _handle_event(self, event):
		'''
		This method handles each individual event, checking if the
		user has Quit the game, resized the windows, or pressed
		any keys.
		'''
		if event.type == pygame.QUIT:
			self._running = False
		elif event.type == pygame.VIDEORESIZE:
			self._create_surface(event.size)
		elif event.type == pygame.KEYDOWN:
			self._handle_keys(event)

	def _handle_keys(self, event: 'pygame.EVENT'):
		'''
		This method checks if there is an existing faller
		that has not frozen yet, and if so moves it left, right, 
		or rotates it. There is also an additional feature that
		allows fallers to fall at an accelerated rate when the 
		down arrow button is pressed.
		'''

		if (self._game_state.get_faller()!= None) and (self._game_state.get_faller().get_state()!= columns.EMPTY) and (self._game_state.get_faller().get_state()!= columns.FROZEN):
			if event.key == pygame.K_LEFT:
				self._game_state.get_faller().move(-1)

			if event.key == pygame.K_RIGHT:
				self._game_state.get_faller().move(1)

			if event.key == pygame.K_SPACE:
				self._game_state.get_faller().rotate()

			if event.key == pygame.K_DOWN:
				#to make testing easier
				self._game_state.get_faller().fall(self._game_state)

	def _draw_board(self):
		'''
		This module displays the board reflecting
		the current state of the game.
		'''
		self._surface.fill(_BACKGROUND_COLOR)
		self._draw_grid()
		self._draw_jewels()
		pygame.display.flip()

	def _grid_coordinates_to_pixel(self):
		'''
		This method converts the list containing
		the coordinates needed to draw the grid representing
		the columns and rows of the game board from
		fractional to pixelated coordinates.
		'''

		self._horizontal_pixel_grid_coordinates = []
		self._vertical_pixel_grid_coordinates = []

		for point in _HORIZONTAL_GRID_FRAC_POINTS:
			x, y = point
			self._horizontal_pixel_grid_coordinates.append((self._frac_x_to_pixel_x(x), self._frac_y_to_pixel_y(y)))

		for point in _VERTICAL_GRID_FRAC_POINTS:
			x, y = point
			self._vertical_pixel_grid_coordinates.append((self._frac_x_to_pixel_x(x), self._frac_y_to_pixel_y(y)))

	def _draw_grid(self):
		'''
		This method draws a grid of 3 pixel wide lines acting as the gameboard.
		The lines change color along a rainbow gradient.
		'''
		self._grid_coordinates_to_pixel()
		self._change_line_color()
		color = pygame.Color(self._colors[0], self._colors[1], self._colors[2])

		for index in range(14):
			pygame.draw.line(self._surface, color, self._horizontal_pixel_grid_coordinates[2*index], self._horizontal_pixel_grid_coordinates[2*index + 1], 3)

		for index in range(7):
			pygame.draw.line(self._surface, color, self._vertical_pixel_grid_coordinates[2*index], self._vertical_pixel_grid_coordinates[2*index + 1], 3)

	def _draw_jewels(self):
		'''
		This draws all the Jewels on the board in a specific way and color.
		If the Jewels are moving they have a yellow background, if they are landed they
		have a green background, and if they match they shrink into a small ellipse before
		disappearing.
		'''
		board = self._game_state.get_board()
		for row in range(_BOARD_ROWS):
			temp = row
			for column in range(_BOARD_COLUMNS):
				row = temp
				diff = 0
				if len(board[column]) > _BOARD_ROWS:
					diff = len(board[column]) - _BOARD_ROWS
					row += diff
				if board[column][row].get_state() == columns.MATCH:
					self._draw_shrunk_jewel(row-diff, column, _COLORS[board[column][row].get_color()], 0.0225)
				elif board[column][row].get_state() == columns.LANDED:
					self._fill_square(row-diff, column, pygame.Color(128, 210, 118))
					self._draw_jewel(row-diff, column, _COLORS[board[column][row].get_color()], 0.0225)
				elif board[column][row].get_state() == columns.MOVING:
					self._fill_square(row-diff, column, pygame.Color(236, 217, 115))
					self._draw_jewel(row-diff, column, _COLORS[board[column][row].get_color()], 0.0225)
				elif board[column][row].get_state() == columns.FROZEN:
					self._fill_square(row-diff, column, _COLORS[board[column][row].get_color()])

	def _draw_shrunk_jewel(self, row : int, column: int, color: 'pygame.COLOR', frac_width: float):
		'''
		This draws a specific Jewel as a small ellipse,
		representing that it is matching with other Jewels.
		'''
		frac_x, frac_y = self._get_top_left_frac(row, column)
		pixel_x = self._frac_x_to_pixel_x(frac_x+.0125)+2.25
		pixel_y = self._frac_y_to_pixel_y(frac_y+.0125)+2.25
		current_width = self._surface.get_width()
		current_height = self._surface.get_height()
		pygame.draw.ellipse(self._surface, color, pygame.Rect(pixel_x, pixel_y, int(current_width*frac_width), int(current_height*frac_width)))
	
	def _draw_jewel(self, row : int, column: int, color: 'pygame.COLOR', frac_width: float):
		'''
		This draws Jewels that are falling or landed as smaller
		than the full square they are in so the background color can be seen.
		'''
		frac_x, frac_y = self._get_top_left_frac(row, column)
		pixel_x = self._frac_x_to_pixel_x(frac_x+.0125)+2.25
		pixel_y = self._frac_y_to_pixel_y(frac_y+.0125)+2.25
		current_width = self._surface.get_width()
		current_height = self._surface.get_height()
		pygame.draw.rect(self._surface, color, pygame.Rect(pixel_x, pixel_y, int(current_width*frac_width), int(current_height*frac_width)))

	def _get_center_frac(self, row : int, column : int) -> float and float:
		'''
		This gets the center coordinates of a cell of a grid given
		its specific row and column. It is used in the case when
		I want to draw circles.
		'''
		temp, y = _HORIZONTAL_GRID_FRAC_POINTS[row*2]
		x, temp = _VERTICAL_GRID_FRAC_POINTS[column*2]
		return x+0.025, y+0.025

	def _fill_square(self, row: int, column: int, color: 'pygame.COLOR'):
		'''
		This method fills a cell specified by its row and column 
		with a particular color.
		'''
		frac_x, frac_y = self._get_top_left_frac(row, column)
		pixel_x = self._frac_x_to_pixel_x(frac_x)+2.25
		pixel_y = self._frac_y_to_pixel_y(frac_y)+2.25
		current_width = self._surface.get_width()
		current_height = self._surface.get_height()
		pygame.draw.rect(self._surface, color, pygame.Rect(pixel_x, pixel_y, int(current_width*0.05)-3, int(current_height*0.05)-3))
	
	def _get_top_left_frac(self, row: int, column: int) -> float and float:
		'''
		This gets the fractional coordinates representing
		the top left corner of a cell given its row and colunn.
		'''
		temp, y = _HORIZONTAL_GRID_FRAC_POINTS[row*2]
		x, temp = _VERTICAL_GRID_FRAC_POINTS[column*2]
		return x, y

	def _frac_x_to_pixel_x(self, frac:float) -> int:
		'''
		This converts a fractional x coordinate to a pixelated
		x coordinate.
		'''
		return int(frac*self._surface.get_width())

	def _frac_y_to_pixel_y(self, frac: float) -> int:
		'''
		This converts a fractional y coordinate to a pixelated
		y coordinate.
		'''
		return int(frac*self._surface.get_height())

	def _change_line_color(self):
		'''
		This updates the game's list of colors
		so it can have a rainbow gradient. 
		'''
		self._get_colors()
	
	def _get_colors(self):
		'''
		This module changes the board's color scheme
		so that it has a rainbow gradient.
		'''

		if (self._colors[self._colors[3]] == 234) or (self._colors[self._colors[3]] == 150):
			if self._colors[3] == 0:
				self._colors[3] = 2
			else:
				self._colors[3] -= 1

		if self._colors[self._colors[3]] == 234:
			self._colors[4] = -2
		elif self._colors[self._colors[3]] == 150:
			self._colors[4] = 2
		
		self._colors[self._colors[3]] += self._colors[4]

	def _initialize_game(self):
		'''
		This prepares the game for it to be played
		by initializing a columns.GameState object with
		an empty board and a randomized faller.
		'''
		empty_board = columns.get_empty_board(_BOARD_ROWS, _BOARD_COLUMNS)
		self._game_state = columns.GameState(empty_board, None, _BOARD_COLUMNS, _BOARD_ROWS)
		self._game_stats = [True, True, 0]
		self._make_random_faller()
		#self._print_board()

	def _make_random_faller(self):
		'''
		Checks if there is a current faller in play and if not
		creates one of a random color and column, then adds it to 
		the board.
		'''
		if (self._game_state.get_faller() == None) or (self._game_state.get_faller().get_state() == columns.EMPTY):
			column = self._get_valid_random_column()
			jewel1 = columns.Jewel(columns.MOVING, columns.COLORS[random.randint(0, 6)])
			jewel2 = columns.Jewel(columns.MOVING, columns.COLORS[random.randint(0, 6)])
			jewel3 = columns.Jewel(columns.MOVING, columns.COLORS[random.randint(0, 6)])

			self._game_state.set_faller(columns.Faller(column, jewel1, jewel2, jewel3, self._game_state))

	def _get_valid_random_column(self) -> int:
		'''
		This method generates a random column for the columns.Faller to reside in
		from all the non-filled columns currently in the board. If all columns are filled
		then a random column will be returned so the game over checker can end the game.
		'''
		column_space = list(range(0, len(self._game_state.get_board())-1))
		for column in range(len(self._game_state.get_board())-1):
			if self._game_state.get_board()[column][0].get_state() != columns.EMPTY:
				column_space.remove(column)

		if len(column_space) == 0:
			return random.randint(0, len(self._game_state.get_board())-1)
		else:
			index = random.randint(0, len(column_space)-1)
			return column_space[index]


 

	def _handle_game_events(self):
		'''
		This method handles all the game-related mechanisms,
		including checking for matches and removing them,
		creating random fallers, and making one "time" frame
		be incremented.
		'''
		if self._game_state.check_matches():
			self._game_state.remove_matches()
		elif (self._game_state.get_faller() == None) or (self._game_state.get_faller().get_state() == columns.EMPTY):
			self._make_random_faller()
		else:
			self._game_state.tick_time()

	def _print_board(self):
		'''
		This function is an extra function used to test
		if the game mechanisms are being displayed properly
		on the window. It displays the game simultaenously 
		with the window on the python sell window.
		'''
		board = self._game_state.get_board()
		for row in range(_BOARD_ROWS):
			temp = row
			print('|', end = '')
			for column in range(_BOARD_COLUMNS):
				row = temp
				if len(board[column]) > _BOARD_ROWS:
					diff = len(board[column]) - _BOARD_ROWS
					row += diff
				if board[column][row].get_state() == columns.EMPTY:
					print('   ', sep = '', end = '')
				elif board[column][row].get_state() == columns.MATCH:
					print(f'*{board[column][row].get_color()}*', end = '')
				elif board[column][row].get_state() == columns.MOVING:
					print(f'[{board[column][row].get_color()}]', end = '')
				elif board[column][row].get_state() == columns.LANDED:
					print(f'|{board[column][row].get_color()}|', end = '')
				else:
					print(f' {board[column][row].get_color()} ', end = '')
			print('|')
		print('', '---'*_BOARD_COLUMNS, '')

def _extend_grid_frac_coordinates():
	'''
	This function adds the rest of the points the global constants
	_HORIZONTAL_GRID_FRAC_POINTS and _VERTICAL_GRID_FRAC_POINTS should
	contain. It's only purpose is to make the initalization of the global
	constants less cluttered, it is NOT used to udpate the global constants.

	The global constants mentioned above are used to draw multiple lines 
	and create a grid for the Columns game.
	'''
	for i in range(_BOARD_ROWS*2):
		x1, y1 = _HORIZONTAL_GRID_FRAC_POINTS[-2]
		_HORIZONTAL_GRID_FRAC_POINTS.append((x1, y1 + 0.05))

	for i in range(_BOARD_COLUMNS*2):
		x2, y2 = _VERTICAL_GRID_FRAC_POINTS[-2]
		_VERTICAL_GRID_FRAC_POINTS.append((x2 + 0.05, y2))

if __name__ == '__main__':
	_extend_grid_frac_coordinates()
	ColumnsGame().run()