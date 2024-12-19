import csv

with open("products.csv", "r") as file:
    data = list(csv.DictReader(file))
    data = sorted(data, key=lambda x: int(x['price']))
    head = list(data[0].keys())
    print(type(head))
    uniquecategory = []
    for i in data:
        uniquecategory.append(i["category"])
    uniquecategory = sorted(list(set(uniquecategory)))

    for i, cat in enumerate(uniquecategory, start=1):
        print(f"{i}. {cat}")
    choice = int(input("\nChoose a category : "))
    print("")

    print("1. Rating")
    print("2. Color")
    print("3. Size")
    print("4. Prize")
    fi = int(input("\nChoose a Filter : "))
    match fi:
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
    uniquefil = []
    for i in data:
        uniquefil.append(i[a])
    uniquefil = sorted(list(set(uniquefil)))
    if fi == 4:
        uniquefil = [int(i) for i in uniquefil]
        uniquefil = sorted(uniquefil)
        min = 11999
        max = 0
        for i in data:
            if i["category"] == uniquecategory[choice - 1]:
                if int(i[a]) < min:
                    min = int(i[a])
                if int(i[a]) > max:
                    max = int(i[a])
        n = min
        for n in range(min, max + 1):
            n = int(input(f"Enter Max prize between {min} and {max} : "))
            if n >= min and n <= max:
                break
        fil = [int(i) for i in uniquefil if min <= int(i) <= n]
        for i, f in enumerate(fil, start=1):
            print(f"{i}. {f}")
        choic = int(input("\nChoose a category : "))
        uniquefil = [str(x) for x in uniquefil]
        fil = [str(x) for x in fil]
        print(fil[choic - 1])
        for i, e in enumerate(uniquefil):
            if e == str(fil[choic - 1]):
                choic = i + 1
                break
        print("")
    else:
        for i, f in enumerate(uniquefil, start=1):
            print(f"{i}. {f}")
        choic = int(input("\nChoose a category : "))
        print("")
    # for i in data:
    # if i["category"] == uniquecategory[choice-1]:
    # if i[a] == uniquefil[choic-1]:
    # print(i["price"], i["category" ], i["product_id"],'  ', i[a], sep='\t')

    print("1. Show max price 10 items")
    print("2. Show min price 10 items")
    print("3. Show top rated 10 items")
    print("4. Show latest 10 items")
    choi = int(input("\nChoose a category : "))
    if choi == 1:
        l = 0
        rdata = sorted(data, key=lambda x: int(x['price']), reverse=True)
        final = {}
        for i in rdata:
            if i["category"] == uniquecategory[choice - 1]:
                if i[a] == uniquefil[choic - 1]:
                    l += 1
                    if l <= 10:
                        print(l, i["title"], sep='\t')
                        if l not in final:
                            final[l] = []
                        final[l].append(i)
                    else:
                        break
    elif choi == 2:
        l = 0
        final = {}
        for i in data:
            if i["category"] == uniquecategory[choice - 1]:
                if i[a] == uniquefil[choic - 1]:
                    l += 1
                    if l <= 10:
                        print(l, i["title"], sep='\t')
                        if l not in final:
                            final[l] = []
                        final[l].append(i)
                    else:
                        break
    elif choi == 3:
        l = 0
        rdata = sorted(data, key=lambda x: int(x['rating']))
        final = {}
        for i in rdata:
            if i["category"] == uniquecategory[choice - 1]:
                if i[a] == uniquefil[choic - 1]:
                    l += 1
                    if l <= 10:
                        print(l, i["title"], sep='\t')
                        if l not in final:
                            final[l] = []
                        final[l].append(i)
                    else:
                        break
    elif choi == 4:
        l = 0
        rdata = sorted(data, key=lambda x: int(x['rating']), reverse=True)
        final = {}
        for i in rdata:
            if i["category"] == uniquecategory[choice - 1]:
                if i[a] == uniquefil[choic - 1]:
                    l += 1
                    if l <= 10:
                        print(l, i["product_id"], i["title"], sep='\t')
                        if l not in final:
                            final[l] = []
                        final[l].append(i)
                    else:
                        break

    else:
        print("Wrong choice.")

if l > 0:
    cho = int(input("Pick a ID : "))
    print("")
    y = final[cho][0]

    for i in head:
        print(f"{i} : {y[i]}")
else:
    print("No Match")
