def main():
    text = shorten(input("Input: "))
    print(f"Output: {text}")


def shorten(word):
    vowels = "aeiou"
    output = ""
    for char in word:
        if char.lower() not in vowels:
            output += char
    return output


if __name__ == "__main__":
    main()
