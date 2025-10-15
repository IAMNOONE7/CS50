from cs50 import get_string

def luhn(num):
    total = 0
    double = False
    for ch in reversed(num):
        d = ord(ch) - 48
        if double:
            d*=2
            total += d//10+d%10
        else:
            total +=d
        double = not double
    return total%10==0

def first_two(num):
    return int(num[:2]) if len(num) >= 2 else int(num[0])


def main():
    num = get_string("Number: ").strip()

    if not num.isdigit():
        print("INVALID")
        return

    numlen = len(num)
    x1 = int(num[0])
    x2 = first_two(num)

    if luhn(num):
        if numlen == 15 and x2 in (34,37):
            print("AMEX")
        elif (numlen == 13 or numlen == 16) and x1 == 4:
            print("VISA")
        elif numlen == 16 and 51<=x2<=55:
            print("MASTERCARD")
        else:
            print("INVALID")
    else:
        print("INVALID")

main()
