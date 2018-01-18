# http://www.thecalculatorsite.com/articles/finance/compound-interest-formula.php
import collections

CI = collections.namedtuple('CI', ['principal', 'rate_of_interest', 'compounding_factor', 'term'])


class CompoundInterest:
    def calculate_interest(self, ci):
        if not ci:
            return None

        if not self.valid(ci):
            return None

        interest = pow((1 + ci.rate_of_interest / ci.compounding_factor), ci.compounding_factor * ci.term)
        return (ci.principal * interest - ci.principal)

    def user_input(self):
        try:
            principal = float(input('Please specify the principal amount -> '))
            rate_of_interest = float(input('Please specify the rate of interest -> '))
            number_of_years = float(input('For how long is the amount invested? ->: '))
            compounding_factor = int(input('Enter the number of times the interest has to be compounded -> '))
            return CI(principal, rate_of_interest, compounding_factor, number_of_years)
        except ValueError:
            print('Invalid input')
            return None

    def valid(self, ci):
        """ this method checks if a 'None' CI object was being passed around by the client of the API
        """
        if ci.rate_of_interest and ci.principal and ci.term and ci.compounding_factor:
            return ci.rate_of_interest >= 0 and ci.principal >= 0 and ci.term >= 0 and ci.compounding_factor > 0
        else:
            return False

    def main(self):
        ci = self.user_input()
        compounded_interest = self.calculate_interest(ci)
        print('The compounded interest for the given input is {}'.format((compounded_interest)))


if __name__ == '__main__':
    CompoundInterest().main()
