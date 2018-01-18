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

                line = line[:-1]
                line = line.replace('.', ' ')
                if line and (line != '\n'):
                    words = line.split(' ')
                    ca.total_word_count += len(words)
                    unique_words += [word for word in words if word not in unique_words]
                    ca.char_count += sum([len(word) for word in words])
                else:
                    ca.blank_line_count += 1
        ca.unique_word_count = len(unique_words)
        return ca
