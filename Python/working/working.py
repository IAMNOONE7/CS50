import re
import sys


def main():
    print(convert(input("Hours: ")))


def convert(s):
    match = re.fullmatch(
        r'\s*(\d{1,2})(?::(\d{1,2}))?\s(AM|PM)\s+to\s+'
        r'(\d{1,2})(?::(\d{1,2}))?\s(AM|PM)\s*',s
    )

    if not match:
        raise ValueError

    hours1, minutes1, merid1, hours2, minutes2, merid2 = match.groups()
    h1 = int(hours1)
    h2 = int(hours2)
    m1 = int(minutes1) if minutes1 is not None else 0
    m2 = int(minutes2) if minutes2 is not None else 0

    if not(1<=h1<=12 and 1<=h2<=12 and 0<=m1<60 and 0<=m2<60):
        raise ValueError

    from_h, from_m = format(h1,m1,merid1)
    to_h, to_m = format(h2,m2,merid2)

    return f"{from_h:02d}:{from_m:02d} to {to_h:02d}:{to_m:02d}"


def format(h,m,merid):
    if merid == "AM":
        h = 0 if h==12 else h
    else:
        h = 12 if h==12 else h+12
    return h,m


if __name__ == "__main__":
    main()
