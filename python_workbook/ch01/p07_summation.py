# Write a program that reads a positive integer, n, from the user and then displays the
# sum of all of the integers from 1 to n. The sum of the first n positive integers can be
# computed using the formula:
# sum = (n)(n + 1)/2


class Summation:
    def user_input(self):
        try:
            return int(input('Please enter a positive number: '))
        except ValueError:
            print('Invalid input')
            return None

    def summation(self, number):
        return int((number * (number + 1) / 2)) if (number and number > 0) else None

    def summation_alt(self, number):
        return sum([x for x in range(0, number + 1)]) if (number and number > 0) else None

    def main(self):
        n = self.user_input()
        print("Summation: {}".format(self.summation(n)))
        print("Summation_alt: {}".format(self.summation_alt(n)))


if __name__ == '__main__':
    Summation().main()
