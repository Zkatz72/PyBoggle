from random import randint
from wordset import Wordset
class BoggleState:
    def __init__(self):
        self._dictionary = Wordset(11)
        self._discovered = {}

        #create the english dictionary
        for word in open('res/words.txt'):
            self._dictionary.insert(word.strip())

        self._create_board()

    def _create_board(self):
        self._board = [['','','',''], ['','','',''] , ['','','',''] , ['','','','']]
        vowels = False

        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for r in range(4):
            for c in range(4):

                new_letter = letters[randint(0,25)]
                if new_letter in 'AEIOU':
                    vowels = True

                self._board[r][c] = new_letter

        if vowels:
            return
        else:
            self._create_board() #will retry if a vowel is not present


    def confirm_word(self, word):
        if self._dictionary.contains(word) and word not in self._discovered:
            score = 0
            if len(word) <= 4:
                score = 1
            elif len(word) == 5:
                score = 2
            elif len(word) == 6:
                score = 3
            elif len(word) == 7:
                score = 4
            else:
                score = 11
            self._discovered[word] = score

        elif word in self._discovered:
            return 'You already found this word'

        else:
            return 'Not a word'

    def get_total_score(self):
        total = 0
        for i,_ in self._discovered:
            total+=i

        return total

    def print_board(self):
        for r in range(4):
            for c in range(4):
                print(self._board[r][c], end = ' ')
            print()

    def get_board(self):
        return self._board