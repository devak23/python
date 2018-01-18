# Create a program that displays your name and complete mailing address formatted in
# the manner that you would usually see it on the outside of an envelope. Your program
# does not need to read any input from the user


class Address:

    def get_address(self):
        address = []
        address.append('Abhay Kulkarni')
        address.append('206, Shiv Shrishti')
        address.append('Behind S. M. Shetty high school')
        address.append('Chandivali (Powai), Andheri (East)')
        address.append('Mumbai 400072')
        address.append('Maharashtra')

        return ', '.join(address)


if __name__ == '__main__':
    print(Address().get_address())
