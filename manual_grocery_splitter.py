
def main():
    roommates = {
        "david": 0,
        "peter": 0,
        "mason": 0,
        "caleb": 0,
        "matthew": 0,
        "lucus": 0
    }

    roommates_items = {
        "david": [],
        "peter": [],
        "mason": [],
        "caleb": [],
        "matthew": [],
        "lucus": []
    }

    costco_items = {}
    while True:
        item = input("Enter costco item (type 'done' to finish): ")

        if item.lower() == 'done':
            break

        cost = float(input(f"Enter the cost for {item}: $"))
        costco_items[item] = cost

        splitting_input = input("Who is splitting this item? (write names separated by spaces. If shared item, type 'all'): ")
        if splitting_input == 'all':
            cost_per_person = cost / 6
            for name in roommates.keys():
                roommates[name] += cost_per_person
                roommates_items[name].append(item)
        else:
            splitting = splitting_input.lower().split()

            for name in splitting:
                if name not in roommates.keys():
                    print(f"Error: {name} is not a valid roommate")
                roommates_items[name].append(item)

            cost_per_person = cost / len(splitting)
            for name in splitting:
                roommates[name] += cost_per_person

    print("Final Breakdown: \n")
    for roommate, owed in roommates.items():
        print(f"{roommate} owes ${owed}")
        print(f"{roommate} is splitting: {roommates_items[roommate]}")


if __name__ == '__main__':
    main()