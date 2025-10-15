import sys
import csv

def main():
    if len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    elif len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")

    in_file = sys.argv[1]
    out_file = sys.argv[2]

    if not in_file.endswith(".csv"):
        sys.exit("Not a CSV file")

    if not out_file.endswith(".csv"):
        sys.exit("Not a CSV file")

    try:
        with open(in_file, newline="", encoding="utf-8") as _file:
            reader = csv.DictReader(_file)
            rows = []

            for row in reader:
                    lastname, firstname = row["name"].split(",")
                    house = row["house"]

                    rows.append({"first": firstname.strip(), "last": lastname.strip(), "house":house})

        with open(out_file, "w", newline="", encoding="utf-8") as _file:
            writer = csv.DictWriter(_file, fieldnames=["first", "last", "house"])
            writer.writeheader()
            writer.writerows(rows)

    except FileNotFoundError:
        sys.exit(f"Could not read {sys.argv[1]}")


main()
