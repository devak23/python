eager_squares = [x * x for x in range(1,11)]

print(eager_squares)

lazy_squares = (x * x for x in range(1,11))

print(lazy_squares)

print(next(lazy_squares))
print(next(lazy_squares))
print(next(lazy_squares))
print(next(lazy_squares))