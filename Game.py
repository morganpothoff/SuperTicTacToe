

from tkinter import *
from tkinter import ttk


class Game(Tk):
	"""
	# has a Board
	# has a state
	# has players
	# has a current player's turn
	# has a winner
	# has a list of turns
	"""
	def __init__(self):
		Tk.__init__(self, screenName="TicTacToe")
		self.geometry("700x700")

		self.board = Board(self)
		self.current_player: int = 0
		# self.turn: int = 0  # [0, 1] for current player

		self.state = State()


	def turn(self, row: int, column: int):
		self.board.replace_button_with_text(row, column, {0: "X", 1: "O"}[self.current_player])
		self.state(row, column)
		self.current_player = not self.current_player

		if(self.state.game_over()):
			print("Game over")

			# Convert remaining buttons to text
			for x, row in enumerate(self.board.boxes):
				for y, value in enumerate(row):
					if(not isinstance(value, Label)):
						self.board.replace_button_with_text(x, y, " ")

			# Convert texts to color
			self.board.configure_boxes(bg={0: "blue", 1: "red"}[not self.current_player])
				# Determine current weenner
				# Set color of all text to color of weenner


class Board(Frame):
	"""
	# has 9 boxes
	"""
	def __init__(self, game: Game):
		Frame.__init__(self, game, bg="Black")
		self.grid()  # Grid self to game(TK)

		self.game: Game = game  # save reference to parent so that we can access it later

		self.boxes = [[None, None, None] for x in range(3)]

		for row in range(3):
			for column in range(3):
				self.boxes[row][column] = Box(self, row, column)


	def replace_button_with_text(self, row: int, column: int, text: str):
		# FROM: https://stackoverflow.com/a/66022800
		self.grid_slaves(row=row, column=column)[0].destroy()
		self.boxes[row][column] = Label(self, text=text, width=5, height=2)
		self.boxes[row][column].grid(row=row, column=column, padx=(4, 4), pady=(4, 4))


	def configure_boxes(self, **kwargs: dict):
		for row in self.boxes:
			for box in row:
				box.config(**kwargs)



class Box(ttk.Button):
	def __init__(self, board: Board, row: int, column: int):
		Button.__init__(self, board, height=2, width=2, text=" ", command=self.on_click)
		self.grid(column=column, row=row, padx=(4, 4), pady=(4, 4))

		self.board: Board = board
		self.row = row
		self.column = column


	def on_click(self):
		self.board.game.turn(self.row, self.column)
		# print(f"CLICKY [{self.row}, {self.column}]")

	# has a value [-, X, O]



class State():
	# based on moves made
	# save the current moves
	def __init__(self, starting_player: int=0):
		self.boxes: list[list[str|None]] = [[None, None, None] for _ in range(3)]
		self.current_player: int = starting_player


	def __call__(self, row: int, column: int):
		# move_coordinate = [ROW, COLUMN]
		# move_coordinate = [0, 1]
		# set value to new move
		self.boxes[row][column] = {0: "X", 1: "0"}[self.current_player]
		self.current_player = not self.current_player

	def game_over(self) -> bool:
		# Trivial reject
		if(sum(1 for row in self.boxes for value in row if(value)) < 5):
			return False

		previous_player = not self.current_player
		# Check horizontal
		for row in self.boxes:
			if(row == [{0: "X", 1: "0"}[previous_player]] * 3):
				return True

		# Check vertical
		symbol = {0: "X", 1: "0"}[previous_player]
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
	game = Game()
	game.mainloop()



if(__name__ == "__main__"):
	main()
