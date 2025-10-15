import emoji

def main():
    text_emoji = input("Input: ")
    _emoji = emoji.emojize(text_emoji, language="alias")
    print(f"Output: {_emoji}")

main()
