from urllib.request import urlopen


def fetch_words(url):
    """
    Fetches a list of words from a given URL
    :param url: The URL containing the utf-8 document
    :return: a list of words contained in the document
    """
    with urlopen(url) as story:
        story_words = []
        for line in story:
            line_words = line.decode('utf-8').split()
            for word in line_words:
                story_words.append(word)

        return story_words


def print_items(items):
    """
    Prints the items that are passed
    :param items: printable items
    :return: None
    """
    for item in items:
        print(item)


def main(url):
    """
    Invokes the main from the command line
    :param url: url of the document passed via sys.args
    :return: None
    """
    words = fetch_words(url)
    print_items(words)


print(__name__)  # displays __main__ if you run via terminal or module name if run via REPL

if __name__ == '__main__':
    import sys
    url = sys.argv[1]  # 'http://sixty-north.com/c/t.txt'
    main(url)
