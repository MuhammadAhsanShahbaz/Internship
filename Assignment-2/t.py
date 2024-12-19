import csv





class Product:
    def __init__(self):
        self.data = self.get_data_from_file()

    def get_data_from_file(self):
        with open("products.csv", "r") as file:
            data = list(csv.DictReader(file))
            return sorted(data, key=lambda x: int(x['price']))

    def actual_working(self):
        if 'a' == 'a':
            file_headers = list(self.data[0].keys())
            data = self.data

            # Getting all categories
            unique_category = []
            for row in data:
                unique_category.append(row.get("category"))

            unique_category = sorted(list(set(unique_category)))

            # Getting choice categories
            for index, category in enumerate(unique_category, start=1):
                print(f"{index}. {category}")

            choice = int(input("\nChoose a category : "))

            # Getting filter choice
            print("\n1. Rating")
            print("2. Color")
            print("3. Size")
            print("4. Prize")
            filter_choice = int(input("\nChoose a Filter : "))
            match filter_choice:
                case 1:
                    chosen_filter = file_headers[7]
                case 2:
                    chosen_filter = file_headers[3]
                case 3:
                    chosen_filter = file_headers[8]
                case 4:
                    chosen_filter = file_headers[5]
                case _:
                    print("Invalid choice.")

            unique_filter = []
            for row in data:
                unique_filter.append(row.get(chosen_filter))
            unique_filter = sorted(list(set(unique_filter)))

            if fi == 4:
                unique_filter = [int(i) for i in unique_filter]
                unique_filter = sorted(unique_filter)
                min = 11999
                max = 0
                for i in data:
                    if i["category"] == unique_category[choice - 1]:
                        if int(i[chosen_filter]) < min:
                            min = int(i[chosen_filter])
                        if int(i[chosen_filter]) > max:
                            max = int(i[chosen_filter])
                n = min
                for n in range(min, max + 1):
                    n = int(input(f"Enter Max prize between {min} and {max} : "))
                    if n >= min and n <= max:
                        break
                fil = [int(i) for i in unique_filter if min <= int(i) <= n]
                for i, f in enumerate(fil, start=1):
                    print(f"{i}. {f}")
                choic = int(input("\nChoose a category : "))
                unique_filter = [str(x) for x in unique_filter]
                fil = [str(x) for x in fil]
                print(fil[choic - 1])
                for i, e in enumerate(unique_filter):
                    if e == str(fil[choic - 1]):
                        choic = i + 1
                        break
                print("")
            else:
                for i, f in enumerate(unique_filter, start=1):
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
                    if i["category"] == unique_category[choice - 1]:
                        if i[chosen_filter] == unique_filter[choic - 1]:
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
                    if i["category"] == unique_category[choice - 1]:
                        if i[chosen_filter] == unique_filter[choic - 1]:
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
                    if i["category"] == unique_category[choice - 1]:
                        if i[chosen_filter] == unique_filter[choic - 1]:
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
                    if i["category"] == unique_category[choice - 1]:
                        if i[chosen_filter] == unique_filter[choic - 1]:
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

            for i in file_headers:
                print(f"{i} : {y[i]}")
        else:
            print("No Match")

def main():
    Product()


if __name__ == '__main__':
    main()
