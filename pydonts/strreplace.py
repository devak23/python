s = "001011010101001"
from_ = "01"
to_ = "10"
s1 = ""
for f, t in zip(from_, to_):
    s1 = s.replace(f, t)
print("orig: {}, final: {}".format(s, s1))

s2 = s.translate({ord("0"): "1", ord("1"): "0"})
print("orig: {}, final: {}".format(s, s2))


from string import ascii_uppercase
print(ascii_uppercase)
translation_table = [i for i in range(91)]
for l in ascii_uppercase:
    translation_table[ord(l)] = 2 * l.lower()

print(translation_table)
print(translation_table[60:70])

print("Hey, what's UP?".translate(translation_table))

trans_table = {"0": "1", "1": "0"}
print ("001011010101001".translate(str.maketrans(trans_table)))

print ("001011010101001".translate(str.maketrans("01","10")))
print ("#0f45cd".translate(str.maketrans("abcdef", "ABCDEF")))
print ("#0 f45cd".translate(str.maketrans("abcdef", "ABCDEF", "# ")))