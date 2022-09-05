# lambda returns a function object.

### Example 1

str1 = 'Mary had a little lamb'
str2 = 'One a penny, two a penny. Hot cross buns'

# this one reverses the string and changes the case to caps
rev_upper = lambda str: str.upper()[::-1]

# this one reverses the string and changes the case to lower
rev_lower = lambda str: str.lower()[::-1]

print(rev_upper(str1))
print(rev_lower(str2))

## Example 2: We can use lambda functions in conditional checks like so...

format_numeric = lambda num: f"{num:e}" if isinstance(num, int) else f"{num:.2f}"
print("Int Formatting: ", format_numeric(5000))
print("Float Formatting: ", format_numeric(888888.97234613))


## Example 3: difference between lambda functions and def

def cube(y):
    return y * y * y


lambda_cube = lambda y: y * y * y

print("Invoking def: ", cube(3))
print("Invoking lambda: ", lambda_cube(3))

### Example 4: Correct usage of lambda.
## Assigning lambdas to names basically just duplicates the functionality of def - and in general, it's best to do
# something a single way to avoid confusion and increase clarity. The legitimate use case for lambda is where you want
# to use a function without assigning it, e.g:

from collections import namedtuple

Person = namedtuple('Person', ['name', 'age'])

friends = [Person('Abhay', 44), Person('Guru', 38), Person('Tejas', 36), Person('Pravin', 35), Person('Ashwani', 37),
           Person('Avinash', 38), Person('Rakshapal', 34)]

sorted_by_name = sorted(friends, key=lambda f: f.name, reverse=True)
print(sorted_by_name)
sorted_by_age = sorted(friends, key=lambda f: f.age)
print(sorted_by_age)

### Example 5: sorting timestamps

timestamps = [
    "2022-04-20 10:07:30",
    "2022-04-20 10:07:28",
    "2022-04-20 10:07:32",
    "2022-04-20 10:08:12",
    "2022-04-20 10:08:22",
    "2022-04-20 10:09:46",
    "2022-04-20 10:10:17",
    "2022-04-20 10:10:58",
    "2022-04-20 10:11:50",
    "2022-04-20 10:13:13",
    "2022-04-20 10:12:13",
    "2022-04-20 10:25:38"
]

timestamps.sort()
print(timestamps)
sorted_ts = sorted(timestamps, reverse=True)
print(sorted_ts)

### Example 6 - Lambda with if else
max_num = lambda a, b: a if (a > b) else b

print(max_num(4,8))