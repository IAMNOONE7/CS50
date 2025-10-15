import sys
import csv
import tabulate

def main():
    if len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")

    elif len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")

    file = sys.argv[1]

    if not file.endswith(".csv"):
        sys.exit("Not a CSV file")

    try:
        with open(file, newline="", encoding="utf-8") as _file:
            reader = csv.DictReader(_file)
            r = list(reader)

    except FileNotFoundError:
        sys.exit("File does not exist")

    print(tabulate.tabulate(r, headers="keys", tablefmt = "grid"))


main()
