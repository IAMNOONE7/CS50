
def main():
    while True:
        try:
            fraction = input("Fraction: ").strip()
            converted = convert(fraction)
            print(gauge(converted))
            break
        except(ValueError, ZeroDivisionError):
            continue

def convert(fraction):
    x_string, y_string = fraction.split("/")
    x = int(x_string)
    y = int(y_string)

    if y == 0:
        raise ZeroDivisionError

    if x > y or x < 0:
        raise ValueError

    return round((x/y)*100)




def gauge(percentage):
    if percentage <= 1:
        return("E")
    elif percentage >= 99:
        return("F")
    else:
        return(f"{percentage}%")


if __name__ == "__main__":
    main()
