p = lambda *anything: print(*anything)


cars = ['Ford', 'Chevy', 'Toyota', 'Tesla']
prices = [20000, 25000, 30000, 50000]
zipped_cars = zip(cars, prices)

p(zipped_cars)          # OP: <zip object at 0x7704fa12d540>
p(type(zipped_cars))    # OP: <class 'zip'>
p(list(zipped_cars))    # OP: [('Ford', 20000), ('Chevy', 25000), ('Toyota', 30000), ('Tesla', 50000)]

# so zip again is a generator, you add that to a list (imperative operation) and it will expand into a list of tuples.
# let's add another dimension to the data called colors

colors = ['red', 'maroon', 'black', 'blue', 'white']
zipped_colored_cars = zip(cars, prices, colors)
p(list(zipped_colored_cars)) # OP: [('Ford', 20000, 'red'), ('Chevy', 25000, 'maroon'), ('Toyota', 30000, 'black'), ('Tesla', 50000, 'blue')]


zipped_colored_cars = zip(cars, prices, colors)
for car, price, color in zipped_colored_cars:
    p(car, price, color)

students = ['Alice', 'Bob', 'Charlie', 'Dan', 'Eve', 'Fred']
scores = [10, 20, 30, 40, 50]

zipped_students = zip(students, scores)
students, scores = zip(*zipped_students)
p(list(students), list(scores)) # OP: ['Alice', 'Bob', 'Charlie', 'Dan', 'Eve'] [10, 20, 30, 40, 50]


stock_index = ["s_and_p", "dow_jones", "nasdaq"]
closing_values = [2470.24, 22000.03, 6312.47]
index_dict = dict(zip(stock_index, closing_values))
p(index_dict)
index_dict2 =  {idx: val for idx, val in zip(stock_index, closing_values)}
p(index_dict2)


data = [1, 2, 3, 4, 5]

doubling = lambda x: x * 2

rounded_sqrt = lambda x: round(x ** 0.5, 2)

pipeline =  zip (
    map(doubling, data),
    map(rounded_sqrt, data)
)

p(list(pipeline))

# this pipeline is exhaustively evaluated in this way. this is not a very efficient and does not scale well as the data grows
# one problem is we are creating intermediate data structures which dont use memory efficiently. A better way to do this
# is to express this as generator comprehension like so

gen_pipeline = zip(
    (
        doubling(x),
        rounded_sqrt(x)
    )
    for x in data
)

# this pipeline exists in memory. We need to either make it imperative using list() or call next()

p(next(gen_pipeline))

# the structure of gen_pipeline is exactly the same as we apply the same transformations but it is significantly more
# efficient than the previous implementation