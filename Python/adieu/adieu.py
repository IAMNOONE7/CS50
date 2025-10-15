import inflect

def main():
    names = []
    try:
        while True:
            name = input("Name: ")
            names.append(name)

    except EOFError:
        print()

    p = inflect.engine()
    _adieu = p.join(names)
    print (f"Adieu, adieu, to {_adieu}")

main()
