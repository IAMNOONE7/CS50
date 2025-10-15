import random

def main():

    while True:
        try:
            n = int(input("Level: "))
            if n > 0:
                level = n
                break
        except ValueError:
            continue


    _random = random.randint(1, level)


    while True:
        try:
            guess = int(input("Guess: "))
            if guess <=0:
                continue

            if guess < _random:
                print("Too small!")
            elif guess > _random:
                print("Too large!")
            else:
                print("Just right!")
                break
        except ValueError:
            continue


main()
