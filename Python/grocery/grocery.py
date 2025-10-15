def main():
    groc_list = {}

    while True:
        try:
            item = input()
            if not item:
                continue
            _item = item.strip().lower()
            groc_list[_item] = groc_list.get(_item,0)+1

        except EOFError:
            break


    for item in sorted(groc_list):
        print(f"{groc_list[item]} {item.upper()}")

main()
