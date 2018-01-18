import re


def main():
    # 1. Grouping with Parentheses
    print("---------------------- 1. Grouping with Parentheses --------------------------")
    mobile_pattern = re.compile('(\d\d\d)-(\d\d\d\-\d\d\d\d)')
    mo = mobile_pattern.search('My phone number is 513-234-4545')
    for group in mo.groups():
        print(group)

    # 2. Matching Multiple Groups with the Pipe
    print("---------------------- 2. Matching Multiple Groups with the Pipe --------------------------")
    hero_pattern = re.compile(r'Batman|Tina Fey')
    hero = hero_pattern.search('The principal characters\n\n are -- (drum roll)\n\n Batman and Tina Fey')
    print(hero.group())
    print(hero.group())

    hero = hero_pattern.search('Tina Fey likes the Batman movies')
    print(hero.group())
    print(hero.group())

    bat_regex = re.compile(r'Bat(man|mobile|pod|bat)')
    text = 'The Batman owns a Batmobile and a Batpod.\r\nThe Batbat itself is very impressive'
    for match in bat_regex.finditer(text):
        print(match.group())
        print(match.group(1))

    # 3. Optional Matching with the Question Mark
    print("---------------------- 3. Optional Matching with the Question Mark --------------------------")
    bat_regex = re.compile(r'Bat(wo)?man')
    match = bat_regex.search('The adventures of Batman')
    print(match.group())

    match = bat_regex.search('The adventures of Batwoman')
    print(match.group())

    # 4. Matching Zero or More with the asterisk character
    print("---------------------- 4. Matching Zero or More with the asterisk character --------------------------")
    bat_regex = re.compile(r'Bat(wo)*man')
    print(bat_regex.search('The adventures of Batman').group())
    print(bat_regex.search('The adventures of Batwowowowoman').group())

    # 5. Matching One or More with the Plus
    print("---------------------- 5. Matching One or More with the Plus --------------------------")
    bat_regex = re.compile('Bat(wo)+man')
    print(bat_regex.search('The adventures of Batwoman').group())
    print(bat_regex.search('The adventures of Batwowowowoman').group())
    match = bat_regex.search('The adventures of Batman')
    print('No match found') if not match else print(match.group())

    # 6. Matching Specific Repetitions with Curly Brackets
    print("---------------------- 6. Matching Specific Repetitions with Curly Brackets --------------------------")
    ha_reg = re.compile(r'((H|h)a){3}')
    print(ha_reg.search('HaHaHa').group())
    print(ha_reg.search('Hahaha').group())

    # 7. Greedy Matching
    print("---------------------- 7. Greedy Matching --------------------------")
    ha_reg = re.compile('(Ha){3,5}')
    print(ha_reg.search('HaHaHa').group())
    print(ha_reg.search('HaHaHaHa').group())
    print(ha_reg.search('HaHaHaHaHa').group())

    # 8. Non-Greedy Matching
    print("---------------------- # 8. Non-Greedy Matching --------------------------")
    ha_reg = re.compile('(Ha){3,5}?')
    print(ha_reg.search('HaHaHa').group())
    print(ha_reg.search('HaHaHaHa').group())
    print(ha_reg.search('HaHaHaHaHa').group())


if __name__ == '__main__':
    main()
