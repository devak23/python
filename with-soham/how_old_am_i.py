from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils.animated_input import animated_input, animated_message

choice = animated_input ('\nHi, my name is Jarvis. I can find out the age of a person if I know their date of birth. Would you like to try? (Y/N): ')

while choice == 'Y' or choice == 'y':
    user_name = animated_input("Please enter the name of the person: ")
    user_input = animated_input("Please enter their date of birth in DD-MM-YYYY format: ")

    user_date = datetime.strptime(user_input, "%d-%m-%Y")
    current_date = datetime.now()
    diff = current_date - user_date

    relative_diff = relativedelta(current_date, user_date)

    days_lived_so_far = diff.days
    years_lived_so_far = relative_diff.years
    months_lived_so_far = relative_diff.years * 12 + relative_diff.months

    animated_message(f"\n{user_name} has lived for {years_lived_so_far} years and {relative_diff.months} months and {relative_diff.days} days starting from the date of birth: {user_input}.")
    animated_message(f"\nIn terms of days, {user_name} has lived an astounding {days_lived_so_far} days so far. ")
    animated_message(f"\nIn terms of months {user_name} has lived for {months_lived_so_far} months so far.\n\n")

    choice = animated_input("Would you like me to find out the age of anyone else? (Y/N): ")
    if choice == "Y" or choice == "y":
        continue
    else:
        break

animated_message('Thanks for coming. Bye bye!\n\n')
