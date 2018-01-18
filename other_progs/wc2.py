class ContentAnalysis:
    def __init__(self):
        self.line_count = 0 # count the total number of lines in the file
        self.char_count = 0 # count the number of characters in the file
        self.total_word_count = 0   # count the total word count in the file
        self.unique_word_count = 0  # count the number of unique words in the file
        self.white_space_count = 0  # count the number of whitespace in the file
        self.blank_line_count = 0   # count the number of blank lines in the file
        self.content = []


class WordCount:
    def analyze_file(self, file_path):
        if not file_path:
            return None

        ca = ContentAnalysis()
        unique_words = []
        with open(file_path, 'r') as fp:
            for line in iter(fp.readline, ''):
                ca.content.append(line)
                ca.line_count += 1
                if line and line != '\n':
                    word_count, char_count, space_count = self.analyze_line(line, unique_words)
                    ca.total_word_count += word_count
                    ca.white_space_count += space_count
                    ca.char_count += char_count
                else:
                    ca.blank_line_count += 1

        ca.unique_word_count = len(unique_words)
        return ca

    def analyze_line(self, line, unique_words):
        """ the line analysis gives you:
        1. number of words
        2. number of spaces
        3. number of unique words
        4. number of characters
        """

        # chop off the new line character
        line = line[:-1]

        # remove punctuation (period) from the line
        line.replace('.', '')

        # gives the word_count
        words = line.split(' ')
        word_count = len(words)

        # char count
        char_count = sum([len(word) for word in words])

        # unique word check
        if unique_words:
            unique_words.append([word for word in words if word not in unique_words])

        # space count - eliminate alphabets from the line to get spaces
        space_count = len(line.split('\w'))

        return (word_count, char_count, space_count)
