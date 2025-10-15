import sys


def main():
    if len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")

    elif len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")

    file = sys.argv[1]

    if not file.endswith(".py"):
        sys.exit("Not a Python file")

    try:
        with open(file, "r") as _file:
            count = 0
            for line in _file:
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped.startswith("#"):
                    continue
                count +=1

    except FileNotFoundError:
        sys.exit("File does not exist")

    print(count)


main()
