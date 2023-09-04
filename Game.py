

from tkinter import *
from tkinter import ttk


class Coordinate:
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y
		self.row = x
		self.column = y


class SuperGame(Tk):
	def __init__(self):
		Tk.__init__(self, screenName="TicTacToe")
		self.geometry("700x700")

		self.frame = Frame(self, bg="Orange")
		self.frame.grid()

		self.current_player: int = 0
		self.state = State()
		self.games = [[None, None, None] for x in range(3)]
		for row in range(3):
			for column in range(3):
				self.games[row][column] = Game(self, Coordinate(row, column))


	def turn(self, game_coordinate: Coordinate, box_coordinate: Coordinate):
		self.games[game_coordinate.row][game_coordinate.column].turn(box_coordinate, self.current_player)
		self.current_player = not self.current_player
		if(self.games[game_coordinate.row][game_coordinate.column].state.game_over()):
			self.state(game_coordinate, self.current_player)
			print("Game over...?")

		if(self.state.game_over()):
			print("HEERRE")
			pass
			# Handle game over



class Game(Frame):
	"""
	# has a Board
	# has a state
	# has players
	# has a current player's turn
	# has a winner
	# has a list of turns
	"""
	def __init__(self, super_game: SuperGame, coordinate: Coordinate):
		Frame.__init__(self, super_game.frame, bg="Yellow")
		self.grid(row=coordinate.row, column=coordinate.column)

		self.super_game = super_game

		self.coordinate: Coordinate = coordinate

		self.board = Board(self)
		self.state = State()



	def turn(self, box_coordinate: Coordinate, current_player: int):
		self.board.replace_button_with_text(box_coordinate, {0: "X", 1: "O"}[current_player])
		self.state(box_coordinate, current_player)

		if(self.state.game_over()):
			print("Game over")

			self.board.replace_all_buttons_with_text()
			# Convert texts to color
			self.board.configure_boxes(bg={0: "blue", 1: "red"}[current_player])



class Board(Frame):
	"""
	# has 9 boxes
	"""
	def __init__(self, game: Game):
		Frame.__init__(self, game, bg="Black")
		self.grid(row=0, column=0)  # Grid self to game(Frame)

		self.game: Game = game  # save reference to parent so that we can access it later

		self.boxes = [[None, None, None] for x in range(3)]

		for row in range(3):
			for column in range(3):
				self.boxes[row][column] = Box(self, Coordinate(row, column))


	def replace_all_buttons_with_text(self, text: str=""):
			# Convert remaining buttons to text
			for x, row in enumerate(self.boxes):
				for y, value in enumerate(row):
					if(not isinstance(value, Label)):
						self.replace_button_with_text(Coordinate(x, y), text)


	def replace_button_with_text(self, coordinate: Coordinate, text: str):
		# FROM: https://stackoverflow.com/a/66022800
		self.grid_slaves(row=coordinate.row, column=coordinate.column)[0].destroy()
		self.boxes[coordinate.row][coordinate.column] = Label(self, text=text, width=5, height=2)
		self.boxes[coordinate.row][coordinate.column].grid(row=coordinate.row, column=coordinate.column, padx=(4, 4), pady=(4, 4))


	def configure_boxes(self, **kwargs: dict):
		for row in self.boxes:
			for box in row:
				box.config(**kwargs)



class Box(Button):
	def __init__(self, board: Board, coordinate: Coordinate):
		Button.__init__(self, board, height=2, width=2, text=" ", command=self.on_click)
		self.grid(column=coordinate.column, row=coordinate.row, padx=(4, 4), pady=(4, 4))

		self.board: Board = board
		self.coordinate = coordinate


	def on_click(self):
		self.board.game.super_game.turn(self.board.game.coordinate, self.coordinate)
		# print(f"CLICKY [{self.row}, {self.column}]")

	# has a value [-, X, O]



class State():
	# based on moves made
	# save the current moves
	def __init__(self, starting_player: int=0):
		self.boxes: list[list[str|None]] = [[None, None, None] for _ in range(3)]


	def __call__(self, coordinate: Coordinate, current_player: int):
		# move_coordinate = [ROW, COLUMN]
		# move_coordinate = [0, 1]
		# set value to new move
		self.boxes[coordinate.row][coordinate.column] = {0: "X", 1: "O"}[current_player]


	def game_over(self) -> bool:
		# Trivial reject
		if(sum(1 for row in self.boxes for value in row if(value)) < 5):
			return False

		for symbol in ["X", "O"]:
			# Check horizontal
			for row in self.boxes:
				if(row == [symbol] * 3):
					return True

			# Check vertical
			for column in range(len(self.boxes)):
				if(all(self.boxes[row][column] == symbol for row in range(len(self.boxes)))):
					return True

			# Check diagonal
			for diagonal in [[[0, 0], [1, 1], [2, 2]], [[0, 2], [1, 1], [2, 0]]]:
				if(all(self.boxes[row][column] == symbol for row, column in diagonal)):
					return True

		return False


# class Player:
	# has a value [X, O]

# class Turn:
	# is a reference to a play



def main():
	super_game = SuperGame()
	super_game.mainloop()



if(__name__ == "__main__"):
	main()
