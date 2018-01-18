# Write a program that asks the user to enter his or her name. The program should
# respond with a message that says hello to the user, using his or her name.


class Greeter:
    def greet(self):
        print("Hi there!")
        name = input("What's your name? ")
        print("Hello %s. It's nice to meet you :)" % name)


if __name__ == '__main__':
    Greeter().greet()
