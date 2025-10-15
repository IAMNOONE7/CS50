from cs50 import get_string


def count_letter(text):
    return sum(1 for c in text if c.isalpha())

def count_words(text):
    return len(text.split())

def count_sentences(text):
    return sum(1 for c in text if c in ".!?")

def main():
    text = get_string("Text: ")

    l = count_letter(text)
    w = count_words(text)
    s = count_sentences(text)

    _l = l* 100.0 / w
    _s = s* 100.0 / w

    CL = round(0.0588 * _l - 0.296 * _s -15.8)

    if CL >= 16:
        print("Grade 16+")
    elif CL < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {CL}")

main()
