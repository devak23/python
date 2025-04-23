p = lambda anything: print(anything)

first_names = ['mandy', 'bobby', 'charlie']
last_names = ['smith', 'fischer', 'brown']

cap = lambda s: s.capitalize()
joined = map(lambda x, y: cap(x) + ' ' + cap(y), first_names, last_names)
p(list(joined))
