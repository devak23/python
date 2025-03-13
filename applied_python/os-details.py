import os

def getchar() -> None:
    # It's not possible in Python to read a character without having to type the return key as well. On the other hand
    # this is very easy on the Bash shell. The Bash command read -n 1 waits for a key (any key) to be typed.
    # If you import os, it's easy to write a script providing getch() by using os.system() and the Bash
    # shell. getch() waits just for one character to be typed without a return...
    os.system("bash -c \"read -n 1\"")


def listingFiles() -> str:
    # The previous script harbours a problem. You can't use the getch() function, if you are interested in the key
    # which has been typed, because os.system() doesn't return the result of the called shell commands.
    # We show in the following script, how we can execute shell scripts and return the output of these scripts into
    # python by using os.popen()
    dir = os.popen("ls").readlines()
    print(dir)

def details() -> None:
    print(os.name)
    print(f"PWD: {os.getcwd()}")
    os.chdir("/home/abhay/Documents")
    print(f"new directory: {os.getcwd()}")
    print(os.listdir())
    print(f"cpu's = {os.cpu_count()}")
    print(f"pid = {os.getpid()}, ppid = {os.getppid()}, loginName = {os.getlogin()}")


if __name__ == '__main__':
    details()
    #getchar()
    listingFiles()
    #os.system('Chess-rating.png')

    import subprocess
    x = subprocess.Popen(['touch', 'xyz'])
    print(x)
    print(x.poll())
    print(x.returncode)
