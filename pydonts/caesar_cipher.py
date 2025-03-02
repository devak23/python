from string import ascii_uppercase

ALPHABETS = ascii_uppercase


def caesar(text, shift):
    return text.translate(str.maketrans(ALPHABETS, ALPHABETS[shift:] + ALPHABETS[:shift]))


if __name__ == '__main__':
    print(caesar("MARY HAD A LITTLE LAMB", 3))
    print(caesar("HELLO WORLD", 7))