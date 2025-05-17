things_i_like = ["football", "video games", "drawing", "beach playing", "tasty food", "super cars", "cartoons", "Watching Netflix & Youtube", "Birthday parties", "Going to malls", "Songs"]
#                    0          1               2           3               4           5               6

print(len(things_i_like)) # 7


index = 1 # plural of index = indices
print(things_i_like[index])
index = 2
print(things_i_like[index])
index = 3
print(things_i_like[index])

print("=======================================")

for i in range(len(things_i_like)):
    print(i, things_i_like[i])

print("=======================================")

for thing in things_i_like:
    print(thing)

print("============ while loop ===========")
i = 0
while i < 7:
    print(i, things_i_like[i])
    i = i + 1


primes = []
for i in range(2,101):
    if i == 3 or i == 5 or i == 7:
        primes.append(i)
        continue

    indivisible: bool = False
    for prime in primes:
        if i % prime == 0 or i % 2 == 0:
            break
        else:
            indivisible = True

    if indivisible:
        primes.append(i)

print(primes)