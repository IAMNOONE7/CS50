def main():
    while True:
        fraction = input("Fraction: ").strip()
        try:
            x_string, y_string = fraction.split("/")
            x = int(x_string)
            y = int(y_string)

            if y <= 0 or x > y or x < 0:
                raise ValueError

            percentage = round((x/y)*100)
            break
        except(ValueError, ZeroDivisionError):
            # No Error message in the assignment
            continue

    if percentage <= 1:
        print("E")
    elif percentage >= 99:
        print("F")
    else:
        print(f"{percentage}%")


main()
