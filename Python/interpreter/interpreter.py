def main():
    expression = input("Expression: ")
    x,y,z = expression.split()

    x=int(x)
    z=int(z)

    if y == "+":
        result = x + z
    elif y == "-":
        result = x - z
    elif y == "*":
        result = x * z
    elif y == "/":
        result = x / z
    else:
        print("Not valid Operator")
        return
    print(f"{result:.1f}")


main()
