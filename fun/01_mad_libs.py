p = lambda *anything: print(*anything)

def get_story(adjective1: str, noun1: str, verb1: str, noun2: str, verb2: str) -> str:
    return f"""
Once upon a time, there was a {adjective1} {noun1} who loved to {verb1} all day. One day, {noun2} walked into the room and saw {noun1} {verb1}ing. 

{noun2}: "What are you doing?"
{noun1}: "I'm just {verb1}ing, what's the big deal?"
{noun2}: "Well, it's not every day that I see you {verb1}ing in the middle of the day."
{noun1}: "I guess you're right. Maybe I should take a break from {verb1}ing."
{noun2}: "That's probably a good idea. Why don't we go {verb2} instead?"
{noun1}: "Sure, that sounds like fun!"

And so, {noun2} and the {noun1} went off to {verb2} and had a great time. 
The end.    
    """


def main() -> None:
    noun1: str = input("Enter the name of character1: ")
    noun2: str = input("Enter the name of character2: ")
    verb1: str = input(f"What was {noun1} doing (sleep/walk/play/code...)?: ")
    verb2: str = input(f"What was {noun2} doing (sleep/walk/play/code...)?: ")
    adjective1: str = input(f"how would descibe quality of {noun1} (lazy/sleepy/active/sharp/stupid...)?: ")

    story = get_story(adjective1, noun1, verb1, noun2, verb2)
    p(story)

if __name__ == '__main__':
    main()