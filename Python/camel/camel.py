camel_text = input("camelCase: ")
snake_text = ""

for char in camel_text:
    if char.isupper():
        snake_text += "_" + char.lower()
    else:
        snake_text += char

print(f"snake_case: {snake_text}")
