import threading
import time

barrier = threading.Barrier(4)

def play(name):
    print(f"{name} has started")
    score = 0
    for i in range(5):
        time.sleep(3)
        print(f"{name} is playing")

    # barrier
    barrier.wait()

    # code for session killing
    # code for displaying final results
    print(f"{name} has scored {score} points")
    # code for sending winning amount to accounts
    print(f"sending winning amount to {name}'s account")

Threads = []
players = ['Raj', 'Saylee', 'Jay', 'Ayesha']
for player in players:
    p = threading.Thread(target=play, args=(player,))
    Threads.append(p)
    p.start()
