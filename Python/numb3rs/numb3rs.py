import re
import sys


def main():
    print(validate(input("IPv4 Address: ")))


def validate(ip):
    octet = r'(25[0-5]|2[0-4]\d|1?\d?\d)'
    pattern = rf'^{octet}\.{octet}\.{octet}\.{octet}$'
    if re.fullmatch(pattern, ip):
        return True
    else:
        return False

if __name__ == "__main__":
    main()
