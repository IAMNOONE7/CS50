def main():
    money = value(input("Greeting: ").lstrip().lower())
    print(f"{money}")

def value(greeting):
    _greeting = greeting.lstrip().lower()

    if _greeting.startswith("hello"):
        money = 0
    elif _greeting.startswith("h"):
        money = 20
    else:
        money = 100

    return money


if __name__ == "__main__":
    main()
