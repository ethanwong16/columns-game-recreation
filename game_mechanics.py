#10525263 Ethan Wong
#columns.py

'''
This module implements the "model" of the 
Columns game.
'''
#states
FROZEN = 0
MATCH = 1
MOVING = 2
LANDED = 3
EMPTY = None

COLORS = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']

#jewel color = S, T, V, W, X, Y, Z
#jewel state = frozen, faller, match
#faller state = moving, landed, frozen


class NonExistentColumnError(Exception):
	'''
	An error signifying a certain column is non-existent
	'''
	pass

class InvalidMoveError(Exception):
	'''
	An error signifying a certain move is invalid
	'''
	pass

class InvalidColorError(Exception):
	'''
	An error signifying an invalid Jewel
	color.
	'''
	pass

class Jewel:
	'''
	This class represents individual Jewel objects.
	'''
	def __init__(self, state: int, color: str):
		self._color = color
		self._state = state

	def get_color(self):
		'''
		This method returns the jewel's color.
		'''
		return self._color

	def get_state(self):
		'''
		This method returns the jewel's state.
		'''
		return self._state

	def set_state(self, state: int):
		'''
		This method changes the jewel's state.
		'''
		self._state = state

	def is_matchable(self) -> bool:
		'''
		This method checks if the Jewel is in the right
		state to be matched.
		'''
		return self._state == FROZEN or self._state == MATCH

class Faller:
	'''
	This class represents a faller object.
	'''
	def __init__(self, column: int, j1: Jewel, j2: Jewel, j3: Jewel, game_state: 'GameState'):
		self._jewels = [j1, j2, j3]
		self._column = column
		self._row = -1
		self._state = MOVING
		self._frozen_out_of_bounds = True
		self._game_state = game_state

		#checking for errors with creating faller objects

		if game_state.check_matches():
			raise InvalidMoveError('You cannot make the move at this time.')
		if column not in range(len(game_state.get_board())):
			raise NonExistentColumnError('This column is out of bounds.')
		for jewel in self._jewels:
			if jewel.get_color() not in COLORS:
				raise InvalidColorError('Color(s) are not valid. Valid jewel colors are S, T, V, W, X, Y, Z')

	def rotate(self):
		'''
		This method rotates the faller.
		'''
		self._jewels[0], self._jewels[1], self._jewels[2] = self._jewels[2], self._jewels[0], self._jewels[1]

		temp = -1
		for row in range(self._row, self._row-3 , -1):
			if row > -1:
				self._game_state.get_board()[self._column][row] = self._jewels[temp]
			temp -= 1

	def get_row(self):
		'''
		This method gives the bottom most row position of hte faller.
		'''
		return self._row

	def get_column(self):
		'''
		This method gives the faller's column.
		'''
		return self._column

	def get_jewels(self):
		'''
		This method gives the jewels within the faller.
		'''
		return self._jewels

	def get_state(self):
		'''
		This method gives the state of the faller.
		'''
		return self._state

	def set_state(self, state: int):
		'''
		This method sets the state of the faller.
		'''
		self._state = state

	def fall(self, game_state: 'GameState') -> bool:
		'''
		This method goes through one iteration of the faller object falling.
		It adjusts its state as necessary and returns a bolean
		signifiying whether it is in a condition where a faller is
		out of bounds from the board.
		'''
		boolean = True

		if self._state == FROZEN:
			self._state = EMPTY
			return False
		elif self._state == LANDED:
			self._state = FROZEN
			if self._row < 2:
				boolean = False
				#need to check if there are matching elements before
				#	you claim that the game is over
		elif self._row+1 < len(game_state.get_board()[self._column])-1:
			if self._row == -1 and (game_state.get_board()[self._column][self._row+1].get_state() != EMPTY):
				self._state = FROZEN
				boolean = False
			elif game_state.get_board()[self._column][self._row+1].get_state() != EMPTY:
				self._state = LANDED
			else:
				self._row += 1
				if game_state.get_board()[self._column][self._row+1].get_state() != EMPTY:
					self._state = LANDED
		else:
			#reached bottom
			self._row += 1
			self._state = LANDED

		game_state._remove_old_fallers()

		for jewel in self.get_jewels():
			jewel.set_state(self._state)

		game_state._update_faller(self)

		self._frozen_out_of_bounds = boolean
		return boolean

	def move(self, direction: int):
		'''
		This moves the faller if it is able to be moved and updates the
		game board and the faller's position.
		'''
		#check faller position
		boolean = True
		if (self._column in range(1, len(self._game_state.get_board())-1)) or (self._column==0 and direction==1) or (self._column==(len(self._game_state.get_board())-1) and direction==-1):
			#check if it is blocked
			for row in range(self._row, self._row-3 , -1):
				if row > -1:
					if self._game_state.get_board()[self._column+direction][row].get_state()!=EMPTY:
						boolean = False
						break
		else:
			boolean = False
		if boolean:
			self._column+=direction
			self._state = LANDED
			if self._row+1<len(self._game_state.get_board()[self._column]) and (self._game_state.get_board()[self._column][self._row+1].get_state()==EMPTY):
				self._state = MOVING

			#update board
			self._game_state._remove_old_fallers()

			for jewel in self.get_jewels():
				jewel.set_state(self._state)

			self._game_state._update_faller(self)
		
		#change position & state of faller
		#remove old faller & update board with new faller

class GameState:
	'''
	This class represents GameState objects.
	'''
	def __init__(self, board: [[Jewel]], faller: Faller, columns: int, rows: int):
		self._board = board
		self._faller = faller
		self._columns = columns
		self._rows = rows

	def get_board(self):
		'''
		This method gives the board.
		'''
		return self._board

	def get_faller(self):
		'''
		This method gives the faller.
		'''
		return self._faller

	def get_columns(self):
		'''
		This method gives the number of columns in the board.
		'''
		return self._columns

	def get_rows(self):
		'''
		This method gives the number of rows in the board.
		'''
		return self._rows

	def set_faller(self, faller: Faller):
		'''
		This method changes the faller of the board.
		'''
		self._faller = faller

	def remove_matches(self):
		'''
		This method pops out matches and updates the board.
		'''
		difference = 0
		for column in range(len(self._board)):
			for row in range(len(self._board[column])):
				row -= difference
				if self._board[column][row].get_state() == MATCH:
					true_column_length = len(self._board[column-1])
					#doesn't matter if column-1 is long, we will still need to add
						# an empty jewel anyways
					self._board[column].pop(row)
					if len(self._board[column]) < true_column_length:
						self._board[column].insert(0, Jewel(EMPTY, None))
					else:
						difference += 1

	def tick_time(self) -> None:
		'''
		This method goes through one iteration of a tick of time
		'''
		check_game_over = True

		if self._faller!= None and (self._faller.get_state()!= EMPTY):
			#let faller continue falling or make faller land
			check_game_over = self._faller.fall(self)


		self.remove_matches()
		#remove matches & check for new ones

		if not check_game_over and (self._faller.get_state() == FROZEN):
			#there is a frozen faller that can't fit into the board
			column = self._faller.get_column()
			row = self._faller.get_row()

			for jewel in self._faller.get_jewels()[:2-row][::-1]:
				self._board[column].insert(0, jewel)

		elif self.get_faller()._state == FROZEN:
			self.get_faller()._state = EMPTY

		self.check_matches()

	def is_game_over(self)-> bool:
		'''
		This checks if the game is over and returns a boolean
		'''
		has_matches = self.check_matches()
		if (not has_matches) and (self._faller!=None):
			if (not self._faller._frozen_out_of_bounds) and (not self._faller.get_state()==None):
				if len(self._board[self._faller.get_column()]) != self._rows:
					self._board[self._faller.get_column()] = self._board[self._faller.get_column()][len(self._board[self._faller.get_column()])-self._rows:]
					return True
		return False
			
	def check_matches(self) -> bool:
		'''
		This  checks for any matches within the board.
		'''
		difference = 0
		final_indexes = []
		for column in range(len(self._board)):
			for row in range(-1, -1*len(self._board[column])-1, -1):
				self._horizontal_matches(column, row, final_indexes)
				self._vertical_matches(column, row, final_indexes)
				self._lower_diagonal(column, row, final_indexes)
				self._upper_diagonal(column, row, final_indexes)

		self._set_matches(final_indexes)

		if len(final_indexes)>0:
			return True
		else:
			return False

	def _horizontal_matches(self, column: int, row: int, final_indexes: [(int, int)]):
		counter = 1
		current_index = [column, row]
		temp_indexes = [tuple(current_index)]

		#check horizontal
		next_index = [column+1, row]

		while (next_index[0]<len(self._board) and (row >= -1*len(self._board[current_index[0]-1])) ):
			if (self._board[current_index[0]][current_index[1]].is_matchable() and self._board[next_index[0]][next_index[1]].is_matchable() and (self._board[current_index[0]][current_index[1]].get_color() == self._board[next_index[0]][next_index[1]].get_color())):
				temp_indexes.append(tuple(next_index)) #convert it for safety , prevent accidental tampering
				counter += 1
				next_index[0] += 1
			else:
				if counter >= 3: 
					final_indexes.extend(temp_indexes)
				temp_indexes = [tuple(next_index)]
				current_index = next_index[::]
				next_index[0] += 1
				counter = 1
		if counter >= 3:
			final_indexes.extend(temp_indexes)

	def _vertical_matches(self, column: int, row: int, final_indexes: [(int, int)]):
		#check vertical
		counter = 1
		current_index = [column, row]
		temp_indexes = [tuple(current_index)]
		next_index = [column, row-1]
		while(next_index[1] >= -1*len(self._board[column])):
			if(self._board[current_index[0]][current_index[1]].is_matchable() and self._board[next_index[0]][next_index[1]].is_matchable() and self._board[current_index[0]][current_index[1]].get_color() == self._board[next_index[0]][next_index[1]].get_color()):
				temp_indexes.append(tuple(next_index)) #convert it for safety , prevent accidental tampering
				counter += 1
				next_index[1] -= 1
			else:
				if counter >= 3: 
					final_indexes.extend(temp_indexes)
				temp_indexes = [tuple(next_index)]
				current_index = next_index[::]
				next_index[1] -= 1
				counter = 1
		if counter >= 3:
			final_indexes.extend(temp_indexes)

	def _lower_diagonal(self, column: int, row: int, final_indexes: [(int, int)]):
		#check lower diagonal
		counter = 1
		current_index = [column, row]
		temp_indexes = [tuple(current_index)]
		next_index = [column+1, row+1]

		while(next_index[0]<len(self._board) and next_index[1]<0 and (row>=-1*len(self._board[current_index[0]+1]))):
			if(self._board[current_index[0]][current_index[1]].is_matchable() and self._board[next_index[0]][next_index[1]].is_matchable() and self._board[current_index[0]][current_index[1]].get_color() == self._board[next_index[0]][next_index[1]].get_color()):
				temp_indexes.append(tuple(next_index)) #convert it for safety , prevent accidental tampering
				counter += 1
				next_index[1] += 1
				next_index[0] += 1
			else:
				if counter >= 3: 
					final_indexes.extend(temp_indexes)
				temp_indexes = [tuple(next_index)]
				current_index = next_index[::]
				next_index[1] += 1
				next_index[0] += 1
				counter = 1
		if counter >= 3:
			final_indexes.extend(temp_indexes)

	def _upper_diagonal(self, column: int, row: int, final_indexes: [(int, int)]):
		#check upper diagonal
		counter = 1
		current_index = [column, row]
		temp_indexes = [tuple(current_index)]
		next_index = [column+1, row-1]
		while(next_index[0]<len(self._board) and (next_index[1] >= -1*len(self._board[next_index[0]])) and (row>-1*len(self._board[current_index[0]+1]))):
			if(self._board[current_index[0]][current_index[1]].is_matchable() and self._board[next_index[0]][next_index[1]].is_matchable() and (self._board[current_index[0]][current_index[1]].get_color() == self._board[next_index[0]][next_index[1]].get_color())):
				temp_indexes.append(tuple(next_index)) #convert it for safety , prevent accidental tampering
				counter += 1
				next_index[1] -= 1
				next_index[0] += 1
			else:
				if counter >= 3: 
					final_indexes.extend(temp_indexes)
				temp_indexes = [tuple(next_index)]
				current_index = next_index[::]
				next_index[1] -= 1
				next_index[0] += 1
				counter = 1
		if counter >= 3:
			final_indexes.extend(temp_indexes)

	def _set_matches(self, final_indexes: [(int, int)]):
		'''
		This changes the baord to have matches.
		'''
		for index in final_indexes:
			self._board[index[0]][index[1]].set_state(MATCH)

	def _remove_old_fallers(self):
		'''
		This gets rid of of old fallers
		'''
		for column in range(len(self._board)):
			for row in range(len(self._board[column])):
				if (self._board[column][row].get_state() == MOVING) or (self._board[column][row].get_state() == LANDED):
					self._board[column][row] = Jewel(EMPTY, None)

	def _update_faller(self, faller: Faller):
		'''
		This updates the board to reflect the current faller status and position
		'''
		temp = -1
		for row in range(faller.get_row(), faller.get_row()-3 , -1):
			if row > -1:
				self._board[faller.get_column()][row] = faller.get_jewels()[temp]
			temp -= 1


def get_empty_board(num_rows: int, num_columns: int) -> [[Jewel]]:
	'''
	This function creates a completely 
	empty board of the specified size
	'''
	board = []
	for column in range(num_columns):
		board.append([])
		for row in range(num_rows):
			board[-1].append(Jewel(EMPTY, None))

	return board