import tkinter as tk
from boggle_model import BoggleState

class BoggleView:

    def __init__(self):
        #added comment to test
        self._root_window = tk.Tk()
        self._root_window.title("Boggle")
        self._game_state = BoggleState()
        self._letter_buttons = []
        self._current_string = ''
        self._label = tk.Label(text = '')
        self._label.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self._root_window.rowconfigure(0, weight=1)
        self._create_board()


        ##need a timer
        # a list of found words
        # 16 buttons
        # label for current string
        # ok button
        #etc.


    def _create_board(self):
        board = self._game_state.get_board()
        letters_frame = tk.Frame(self._root_window, width = 1000, height = 1000)
        for r in range(len(board)):
            for c in range(len(board[0])):
                letter = board[r][c]
                def command(letter):
                    return lambda: self._set_label(self._current_string + letter)
                letter_button = tk.Button(letters_frame,text = letter, command = command(letter))
                letter_button.grid(row = r, column = c, sticky=tk.E+tk.W+tk.N+tk.S)
                self._letter_buttons.append(letter_button)
                letters_frame.columnconfigure(c, weight = 1)
            letters_frame.rowconfigure(r, weight=1)
        letters_frame.grid(row = 1, column = 0, sticky=tk.E+tk.W+tk.N+tk.S)
        self._root_window.columnconfigure(0, weight = 1)
        self._root_window.rowconfigure(1, weight=1)

    def _set_label(self, s):
        self._current_string = s
        self._label.config(text = self._current_string)
    def run(self) -> None:
        self._root_window.mainloop()



if __name__ == '__main__':
    BoggleView().run()
