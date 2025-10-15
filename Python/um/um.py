import re
import sys


def main():
    print(count(input("Text: ")))


def count(s):
    _count = len(re.findall(r'\bum\b', s, flags=re.IGNORECASE))
    return _count


if __name__ == "__main__":
    main()
