import csv

with open("products.csv", "r") as file:
    data = list(csv.DictReader(file))
    data = sorted(data, key=lambda x: int(x['price']))
    head = list(data[0].keys())

    # Getting unique categories
    unique_category = []
    for index in data:
        unique_category.append(index.get("category", ''))
    unique_category = sorted(list(set(unique_category)))

    # Choosing specific category
    for index, category in enumerate(unique_category, start=1):
        print(f"{index}. {category}")
    choice = int(input("\nChoose a category : "))

    # Choosing specific filter
    print("1. Rating")
    print("2. Color")
    print("3. Size")
    print("4. Prize")
    unique_filter_choice = int(input("\nChoose a Filter : "))
    match unique_filter_choice:
        case 1:
            a = head[7]
        case 2:
            a = head[3]
        case 3:
            a = head[8]
        case 4:
            a = head[5]
        case _:
            print("Invalid choice.")

    unique_filter = []
    for index in data:
        unique_filter.append(index[a])
    unique_filter = sorted(list(set(unique_filter)))

    # For price applying some filters
    if unique_filter_choice == 4:
        unique_filter = [int(i) for i in unique_filter]
        unique_filter = sorted(unique_filter)

        min = 11999
        max = 0
        for index in data:
            if index["category"] == unique_category[choice - 1]:
                if int(index[a]) < min:
                    min = int(index[a])
                if int(index[a]) > max:
                    max = int(index[a])

        # Getting price range
        for n in range(min, max + 1):
            n = int(input(f"Enter Max prize between {min} and {max} : "))
            if n >= min and n <= max:
                break

        fil = [int(i) for i in unique_filter if min <= int(i) <= n]

        for index, filter_name in enumerate(fil, start=1):
            print(f"{index}. {filter_name}")
        choic = int(input("\nChoose a category : "))

        unique_filter = [str(x) for x in unique_filter]
        fil = [str(x) for x in fil]
        print(fil[choic - 1])

        for index, e in enumerate(unique_filter):
            if e == str(fil[choic - 1]):
                choic = index + 1
                break
        print("")

    else:
        for index, filter_name in enumerate(unique_filter, start=1):
            print(f"{index}. {filter_name}")
        choic = int(input("\nChoose a category : "))


    print("1. Show max price 10 items")
    print("2. Show min price 10 items")
    print("3. Show top rated 10 items")
    print("4. Show latest 10 items")
    choi = int(input("\nChoose a category : "))
    if choi == 1:
        l = 0
        rdata = sorted(data, key=lambda x: int(x['price']), reverse=True)
        final = {}
        for index in rdata:
            if index["category"] == unique_category[choice - 1]:
                if index[a] == unique_filter[choic - 1]:
                    l += 1
                    if l <= 10:
                        print(l, index["title"], sep='\t')
                        if l not in final:
                            final[l] = []
                        final[l].append(index)
                    else:
                        break
    elif choi == 2:
        l = 0
        final = {}
        for index in data:
            if index["category"] == unique_category[choice - 1]:
                if index[a] == unique_filter[choic - 1]:
                    l += 1
                    if l <= 10:
                        print(l, index["title"], sep='\t')
                        if l not in final:
                            final[l] = []
                        final[l].append(index)
                    else:
                        break
    elif choi == 3:
        l = 0
        rdata = sorted(data, key=lambda x: int(x['rating']))
        final = {}
        for index in rdata:
            if index["category"] == unique_category[choice - 1]:
                if index[a] == unique_filter[choic - 1]:
                    l += 1
                    if l <= 10:
                        print(l, index["title"], sep='\t')
                        if l not in final:
                            final[l] = []
                        final[l].append(index)
                    else:
                        break
    elif choi == 4:
        l = 0
        rdata = sorted(data, key=lambda x: int(x['rating']), reverse=True)
        final = {}
        for index in rdata:
            if index["category"] == unique_category[choice - 1]:
                if index[a] == unique_filter[choic - 1]:
                    l += 1
                    if l <= 10:
                        print(l, index["product_id"], index["title"], sep='\t')
                        if l not in final:
                            final[l] = []
                        final[l].append(index)
                    else:
                        break

    else:
        print("Wrong choice.")

if l > 0:
    cho = int(input("Pick a ID : "))
    print("")
    y = final[cho][0]

    for index in head:
        print(f"{index} : {y[index]}")
else:
    print("No Match")
