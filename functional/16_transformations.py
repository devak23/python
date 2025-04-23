p = lambda anything: print(anything)

first_names = ['anatoly', 'robert', 'borris']
last_names = ['karpov', 'fischer', 'spassky']

cap = lambda s: s.capitalize()
joined_first_last = map(lambda x, y: cap(x) + ' ' + cap(y), first_names, last_names)
p(list(joined_first_last))


middle_initials = ['y', 'r', 'v']
joined_full_names = map(lambda x,y,z: (x + ' '+ y + ' '+z).title(), first_names, middle_initials, last_names)
p(list(joined_full_names))

# builtins
snooker_players = ['Ronnie Sullivan', 'Stephen Hendry', 'Steve Davis', 'John Higgins']
lengths = list(map(len, snooker_players))
dict_snooker_players = dict(zip(snooker_players, lengths))
p(dict_snooker_players)


number_strings = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
p(list(map(int, number_strings)))


from operator import add

a = range(1,5)
b = range(8,20)

p(list(a))
p(list(b))

p(list(map(add, a, b)))