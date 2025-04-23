def square (number: int) -> int:
    return number * number

def double_it(number: int) -> int:
    return number * 2

def sumOfSquares(num1: int, num2: int) -> int:
    return square(num1) + square(num2)

def sumAncesstorSuccessor(num1: int, num2: int) -> int:
    return square(num1-1) + square(num2+1)

def greet(name: str) -> None:
    print (f"Hello, {name}!")

def duplicateList(list):
    if len(list) == 1:
        return [list[0] * 2]
    else:
        return [list[0]* 2] + duplicateList(list[1:])

def mapList(list, action):
    if len(list) == 1:
        return [action(list[0])]
    else:
        return [action(list[0])] + mapList(list[1:], action)

def buildMultiples(factor):
    def internal(value):
        return value * factor
    return internal

def filter(condition, iterable):
    return [item for item in iterable if condition(item)]


import random

def map(function, iterable):
    return [function(item) for item in iterable]

def addPower(superhero) -> None:
    superhero.update(power=random.randint(1, 100))
    return superhero

def againstMan(result, superhero):
    if 'man' in superhero['name'].lower():
        return result + 1
    else:
        return result

if __name__ == '__main__':
    print(sumOfSquares(3, 4))
    print(sumAncesstorSuccessor(3, 4))

    myList = [1, 2, 3, 4]
    print(duplicateList(myList))
    print(mapList(myList, square))

    incrementer = lambda x: x + 1
    print(mapList(myList, incrementer))

    # save the expressions
    multiplesOf3 = buildMultiples(3)
    multiplesOf5 = buildMultiples(5)

    # Evaluate
    print(multiplesOf3(10))
    print(multiplesOf5(10))


    superheroes = [
        {
            'name': 'Batman',
            'editorial': 'DC Comics',
            'alter_ego': 'Bruce Wayne',
            'primary_appearance': 'Detective Comics #27'
        },{
            'name': 'Superman',
            'editorial': 'DC Comics',
            'alter_ego': 'Kal-El',
            'primary_appearance': 'Action Comics #1'
        },{
            'name': 'Spiderman',
            'editorial': 'Marvel Comics',
            'alter_ego': 'Peter Parker',
            'primary_appearance': 'Amazing Fantasy #15'
        },{
            'name': 'Hulk',
            'editorial': 'Marvel Comics',
            'alter_ego': 'Bruce Banner',
            'primary_appearance': 'The Incredible Hulk #1'
        },{
            'name': 'Ironman',
            'editorial': 'Marvel Comics',
            'alter_ego': 'Tony Stark',
            'primary_appearance': 'The Ironman #2'
        }
    ]

    superheroes_dc = filter(lambda superhero: superhero['editorial'] == 'DC Comics', superheroes)
    print(tuple(superheroes_dc))

    superherosPower = map(addPower, superheroes)
    print(tuple(superherosPower))

    import functools
    total = functools.reduce(againstMan, superheroes, 0)
    print(total)

    import random

    print(random.randint(0,100))

    product_powered = lambda x,y, z: (x * y) ** z
    print(product_powered(3,4, 3))
    print(product_powered(5,4, 2))