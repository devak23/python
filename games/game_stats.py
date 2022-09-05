
class GameStats:
    selected_word = None
    AVAILABLE_ATTEMPTS = 8
    current_attempt = 0
    guessed_word = []
    available_chars = [ch for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    used_chars = []

    def __init__(self, selected_word):
        self.selected_word = selected_word

    def print_status(self):
        self.calculate_guessed_word()
        print(self.guessed_word)
        print()
        print(f'You have {(self.AVAILABLE_ATTEMPTS - self.current_attempt)} attempts remaining to guess the word.')
        print(f'You have {self.available_chars} letters to choose from')

    def won(self):
        return ''.join(self.guessed_word) == self.selected_word

    def calculate_guessed_word(self):
        self.guessed_word = [ch if ch in self.used_chars else '_' for ch in self.selected_word]

    def update(self, letter):
        letter = str(letter).upper()
        if self.current_attempt >= self.AVAILABLE_ATTEMPTS and not self.won():
            return -1
        else:
            self.current_attempt = self.current_attempt + 1

        if letter in self.selected_word:
            self.used_chars.append(letter)

        self.available_chars.remove(letter)
        return 0 if self.won() else 1
