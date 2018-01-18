import re


def user_input():
    return input('Please enter a line of text (max 100 characters): ')


def find_pattern(text):
    text = text[:-1] # eliminate the last carriage return
    regex = re.compile(r'[aeiouAEIOU]{2,}')
    for match in regex.finditer(text):
        print(match.group())


def main():
    text = user_input()
    find_pattern(text) if text else print('Text should be limited to 100 characters.')


if __name__ == '__main__':
    main()
