import csv


with open("products.csv", "r") as file:
    data = list(csv.DictReader(file))
    head = list(data[0].keys())
    print(head)
    uniquecategory = []
    for i in data:
        uniquecategory.append(i["category"])
    uniquecategory = sorted(list(set(uniquecategory)))
    print(uniquecategory)
    #for i, cat in enumerate(uniquecategory, start=1):
    #    print(f"{i}. {cat}")
    #choice = int(input("\nChoose a category : "))
    choice = 5
    print(uniquecategory[choice-1])
    print("")

    pdata = {}
    for d in data:
        if d["category"] not in pdata:
            pdata[d["category"]] = []
        pdata[d["category"]].append(d)

    uniqueprize = []
    for i in data:
        uniqueprize.append(i["price"])
    uniqueprize = sorted(list(set(uniqueprize)))
    print(sorted(uniqueprize))
    res = sorted([int(i) for i in uniqueprize])
    print(res)
   # print("1. Rating")
   # print("2. Color")
    #print("3. Size")
    #print("4. Prize")
    #fi = int(input("\nChoose a Filter : "))
    fi = 2
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
    print(a)
    uniquefil = []
    for i in data:
        uniquefil.append(i[a])
    uniquefil = sorted(list(set(uniquefil)))
    print(uniquefil)
    if fi == 4:
        res = [int(i) for i in uniquefil]
        print("min", min(res), "to", max(res))
        #for i, f in enumerate(uniquefil, start=1):
         #   if int(f) in range(min(res), max(res)+1):
          #      print(f"{i}. {f}")
        choic = 20
        #choic = int(input("\nChoose a category : "))
      #  print("")
    else:
        #for i, f in enumerate(uniquefil, start=1):
         #   print(f"{i}. {f}")
        #choic = int(input("\nChoose a category : "))
        choic = 2
        print("")

    for c, record in pdata.items():
        for r in record:
            if c == uniquecategory[choice - 1]:
 #               print(c)
#                print(r[a])
                if r[a] in uniquefil[choic - 1]:
                    print(r["product_id"], '  ', r["title"], '  ', r[a], '   ', r["category"])

    print("1. Show max price 10 items")
    print("2. Show min price 10 items")
    print("3. Show top rated 10 items")
    print("4. Show latest 10 items")
    choi = int(input("\nChoose a category : "))
    if choi == 1:
        p = sorted(res, reverse= True)
        for c, record in pdata.items():
            for r in record:
                if c == uniquecategory[choice - 1]:
                    if r[a] in uniquefil[choic - 1]:
                        print(r["product_id"], '  ', r["title"], '  ', r[a], '   ', r["category"])

    elif choi == 2:
        print(sorted(res))
    elif choi == 3:
        ...
    elif choi == 4:
        ...
    else:
        print("Invalid choice.")

'''
    j = 0
    for i in data:
        if i["category"] == uniquecategory[choice-1]:
            if i[a] in uniquefil[choic-1]:
                print(i["product_id"], '  ', i["title"], '  ', i[a], '   ', i["category"])
                j += 1
            if j == 10:
                break
'''
'''
    for i in data:
        if i[uniquecategory[choice-1]]:
            if i[uniquefil[choic-1]]:
                print(i["product_id"], '  ', i["title"], '  ', i[a], '   ', i["category"])
'''
