from urllib.request import urlopen


def fetch_words(url):
    with urlopen(url) as story:
        story_words = []
        for line in story:
            line_words = line.decode('utf-8').split()
            for word in line_words:
                story_words.append(word)

        return story_words


def print_items(items):
    for item in items:
        print(item)


def main(url):
    words = fetch_words(url)
    print_items(words)


print(__name__)  # displays __main__ if you run via terminal or module name if run via REPL

if __name__ == '__main__':
    import sys
    url = sys.argv[1]  # 'http://sixty-north.com/c/t.txt'
    main(url)
