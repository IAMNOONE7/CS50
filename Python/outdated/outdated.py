def main():
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    while True:
        try:
            date = input("Date: ").strip()

            if "/" in date:
                month, day, year = date.split("/")
                m = int(month)
                d = int(day)
                y = int(year)
                if m>12 or d>31:
                    raise ValueError
                print(f"{y:04}-{m:02}-{d:02}")
                break

            else:
                if "," not in date:
                    raise ValueError
                month, day, year = date.replace(",","").split()
                m = months.index(month.title()) +1
                d = int(day)
                y = int(year)
                if d>31:
                    raise ValueError
                print(f"{y:04}-{m:02}-{d:02}")
                break

        except(ValueError, IndexError):
            continue

main()
