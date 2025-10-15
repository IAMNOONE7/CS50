import requests
import sys

def main():
    if len(sys.argv) != 2:
        sys.exit("Missing command-line argument")

    try:
        n = float(sys.argv[1])
    except ValueError:
        sys.exit("Command-line argument is not a number")


    try:
        r = requests.get("https://rest.coincap.io/v3/assets/bitcoin?apiKey=e2b9c9fdcdfc4fe1e956b42501f511c1c899c1c41d3411d956068ae943f6f495", timeout = 10)
        r.raise_for_status()
        price = float(r.json()["data"]["priceUsd"])
    except:
        sys.exit()


    amount = n * price
    print(f"${amount:,.4f}")


main()
