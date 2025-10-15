def remove_vowels(text):
    vowels = "aeiou"
    output = ""
    for char in text:
        if char.lower() not in vowels:
            output += char
    return output


text = input("Input: ")

print(f"Output: {remove_vowels(text)}")



