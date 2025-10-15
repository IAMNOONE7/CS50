from cs50 import get_int

def main():
    while True:
        Height = get_int("Height: ")
        if 1<= Height <=8:
            break

    for i in range(1, Height +1):
        print(" " * (Height - i), end="")
        print("#" * i, end="")
        print("  ", end="")
        print("#" * i)

main()
