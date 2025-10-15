from datetime import date, datetime
import sys
import inflect


_inflect = inflect.engine()



def calculate_minutes(_date):
    delta = date.today() - _date
    if delta.days < 0:
        sys.exit("Invalid date")
    minutes = round(delta.total_seconds()/60)
    words = _inflect.number_to_words(minutes, andword = "")
    return f"{words.capitalize()} minutes"

def main():
    birth_date = input("Date of Birth: ")
    try:
        parsed_b_d = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except ValueError:
        sys.exit("Invalid date")
    print(calculate_minutes(parsed_b_d))


if __name__ == "__main__":
    main()
