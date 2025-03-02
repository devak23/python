def alternate_casing(text):
    letters = []
    for idx, letter in enumerate(text):
        letters.append(letter.lower() if idx % 2 else letter.upper())

    return "".join(letters)

def alternate_casing2(text):
    return "".join(l.lower() if i % 2 else l.upper() for i, l in enumerate(text))

def alternate_casing3(text):
    letters = []
    [letter.lower() if idx % 2 else letter.upper()
     for idx, letter in enumerate(text)]
    return "".join(letters)

if __name__ == "__main__":
    print(alternate_casing("Mary had a little lamb"))
    print(alternate_casing2("Mary had a little lamb"))