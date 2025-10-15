import re
import sys


def main():
    print(parse(input("HTML: ")))


def parse(s):
    yt = re.search(r'<iframe[^>]+src="https?://(?:www\.)?youtube\.com/embed/([A-Za-z0-9_-]+)[^"]*"', s)
    if not yt:
        return None

    yt_video = yt.group(1)
    return f"https://youtu.be/{yt_video}"





if __name__ == "__main__":
    main()
