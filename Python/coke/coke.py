price = 50
accepted = [25, 10, 5]
inserted = 0

while inserted < price:
    print(f"Amount Due: {price - inserted}")
    money = int(input("Insert Coin: "))
    if money in accepted:
        inserted += money

print(f"Change Owed: {inserted - price}")
